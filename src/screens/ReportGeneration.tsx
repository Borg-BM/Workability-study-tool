// "3. Generate report" from the Stepper flow. The report is a real Word document: the backend
// builds a first draft in Barge Master's report style from the study's data (see ReportSetup and
// backend/app/report_docx.py), then it's written and edited here in a Word-style editor with
// autosave. It can be downloaded to edit in Word and uploaded back. In a revision after one
// that was sent back, the reviewer's comments sit beside the editor to work through.
import { useCallback, useEffect, useRef, useState } from 'react'
import type { DocxEditorRef, Editor } from '@docx-editor.dev/react'
import { canEditStudy, isReviewStage, type Study, type Screen } from '../App'
import type { Identity } from '../identity'
import Stepper from '../components/Stepper'
import ReportDocxEditor, { downloadFile, reportFileName } from '../components/ReportDocxEditor'
import ReportSetup from '../components/ReportSetup'
import ReviewComments from '../components/ReviewComments'
import { Banner, Button, EmptyState, PageBody, PanelHeader, ScreenMessage, TopBar, choiceClass } from '../components/ui'
import { errorMessage, DOCX_MIME, type ApiStudyDetail, generateReportDocx, getReportDocx, getStudyWithReport, saveReportDocx, saveStudyReport } from '../api'
import { SYSTEM_LABELS, defaultReport, mergeReport, type ReportState } from '../reportModel'

type SaveState = 'saved' | 'pending' | 'saving' | 'error'

const SAVE_LABELS: Record<SaveState, string> = { saved: 'All changes saved', pending: 'Unsaved changes…', saving: 'Saving…', error: 'Not saved' }
const AUTOSAVE_DELAY_MS = 1500


export default function ReportGeneration({ study, onNav, currentUser, isAdmin }: { study: Study | null; onNav: (s: Screen) => void; currentUser: Identity; isAdmin: boolean }) {
  const canEdit = Boolean(study && canEditStudy(study, currentUser, isAdmin))
  const [detail, setDetail] = useState<ApiStudyDetail | null>(null)
  const [report, setReport] = useState<ReportState | null>(null)
  const [docx, setDocx] = useState<Uint8Array<ArrayBuffer> | null>(null)
  // Bumped to remount the editor on a document that replaced the current one (generate/upload).
  const [docVersion, setDocVersion] = useState(0)
  const [loaded, setLoaded] = useState(false)
  const [setupOpen, setSetupOpen] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [saveState, setSaveState] = useState<SaveState>('saved')
  const [error, setError] = useState<string | null>(null)
  // An informational line, e.g. that an uploaded file's Word comments were taken out.
  const [notice, setNotice] = useState<string | null>(null)
  const [editor, setEditor] = useState<Editor | null>(null)
  // The previous revision's review comments beside the editor -- open by default while any are.
  const [commentsOpen, setCommentsOpen] = useState(false)
  const [openComments, setOpenComments] = useState(0)

  const editorRef = useRef<DocxEditorRef>(null)
  const fileInput = useRef<HTMLInputElement>(null)
  const dirty = useRef(false)
  const saveTimer = useRef<number | null>(null)
  const saveChain = useRef<Promise<void>>(Promise.resolve())

  useEffect(() => {
    if (!study) return
    setLoaded(false)
    getStudyWithReport(study.id)
      .then(([s, bytes]) => {
        const systemLabel = SYSTEM_LABELS[s.system_type] || s.system_type || 'system'
        const defaults = defaultReport(study, systemLabel)
        setDetail(s)
        setReport(Object.keys(s.report).length > 0 ? mergeReport(defaults, s.report) : defaults)
        setDocx(bytes)
        const previous = s.revisions.find((r) => r.revision === s.revision - 1)
        setCommentsOpen(s.status === 'reporting' && (previous?.open_comment_count ?? 0) > 0)
        setOpenComments(previous?.open_comment_count ?? 0)
        setLoaded(true)
      })
      .catch((err) => setError(errorMessage(err, 'Could not load this study')))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [study?.id])

  // Saves run one at a time; an edit made while one is in flight re-marks the document dirty
  // and gets its own save afterwards.
  const persist = useCallback((): Promise<void> => {
    if (saveTimer.current !== null) {
      window.clearTimeout(saveTimer.current)
      saveTimer.current = null
    }
    if (!study) return saveChain.current
    saveChain.current = saveChain.current.then(async () => {
      if (!dirty.current) return
      dirty.current = false
      setSaveState('saving')
      try {
        const buf = await editorRef.current?.save()
        if (buf) await saveReportDocx(study.id, new Uint8Array(buf))
        setSaveState(dirty.current ? 'pending' : 'saved')
        setError(null)
      } catch (err) {
        dirty.current = true
        setSaveState('error')
        setError(errorMessage(err, 'Could not save the report'))
      }
    })
    return saveChain.current
  }, [study])

  const onEdit = useCallback(() => {
    dirty.current = true
    // docx-editor can report a change mid-render, when React forbids updating this component.
    queueMicrotask(() => setSaveState('pending'))
    if (saveTimer.current !== null) window.clearTimeout(saveTimer.current)
    saveTimer.current = window.setTimeout(() => void persist(), AUTOSAVE_DELAY_MS)
  }, [persist])

  useEffect(() => {
    const warnIfUnsaved = (e: BeforeUnloadEvent) => {
      if (dirty.current) e.preventDefault()
    }
    window.addEventListener('beforeunload', warnIfUnsaved)
    return () => window.removeEventListener('beforeunload', warnIfUnsaved)
  }, [])

  const leave = async (s: Screen) => {
    await persist()
    if (dirty.current && !window.confirm('Your latest changes could not be saved. Leave anyway and lose them?')) return
    onNav(s)
  }

  // Drops any pending autosave and waits out one in flight, so it can't land on top of a
  // document that's about to replace this one.
  const settleSaves = async () => {
    if (saveTimer.current !== null) window.clearTimeout(saveTimer.current)
    saveTimer.current = null
    dirty.current = false
    await saveChain.current
  }

  const replaceDocument = (bytes: Uint8Array<ArrayBuffer>) => {
    setDocx(bytes)
    setDocVersion((v) => v + 1)
    setSaveState('saved')
  }

  const generate = async (next: ReportState) => {
    if (!study) return
    setGenerating(true)
    setError(null)
    try {
      await settleSaves()
      await saveStudyReport(study.id, next as unknown as Record<string, unknown>)
      await generateReportDocx(study.id)
      const [updated, bytes] = await getStudyWithReport(study.id)
      setDetail(updated)
      if (bytes) replaceDocument(bytes)
      setReport(next)
      setSetupOpen(false)
    } catch (err) {
      setError(errorMessage(err, 'Could not generate the report'))
    } finally {
      setGenerating(false)
    }
  }

  const upload = async (file: File) => {
    if (!study || !window.confirm(`Replace the report with "${file.name}"? The current document will be overwritten.`)) return
    try {
      const bytes = new Uint8Array(await file.arrayBuffer())
      await settleSaves()
      const { word_comments_removed: removed } = await saveReportDocx(study.id, bytes)
      // With Word comments in it, what was stored differs from the file: show that version.
      replaceDocument(removed > 0 ? await getReportDocx(study.id) : bytes)
      setNotice(
        removed > 0
          ? `${removed === 1 ? '1 Word comment was' : `${removed} Word comments were`} taken out of "${file.name}": review comments are kept in the app, in the review comments panel.`
          : null
      )
      setError(null)
    } catch (err) {
      setError(errorMessage(err, 'Could not upload that document'))
    }
  }

  const download = useCallback(async () => {
    if (!study) return
    await persist()
    const buf = await editorRef.current?.save()
    if (buf) downloadFile(new Uint8Array(buf), `${reportFileName(study.name)}.docx`, DOCX_MIME)
  }, [study, persist])

  // The document as it is in the editor right now, unsaved edits saved first -- what the
  // review comments are put into for "Download for Word, with comments".
  const currentDocx = useCallback(async () => {
    await persist()
    const buf = await editorRef.current?.save()
    if (!buf) throw new Error('The document is still loading')
    return new Uint8Array(buf)
  }, [persist])

  if (!study || !loaded || !detail || !report) {
    return (
      <div className="flex h-screen bg-bm-shade">
        <Stepper screen="report" status={study?.status ?? 'reporting'} onNav={onNav} />
        <div className="flex-1 flex flex-col min-w-0">
          {study && <TopBar onBack={() => onNav('dashboard')} title={study.name} status={study.status} />}
          <ScreenMessage error={error} />
        </div>
      </div>
    )
  }

  const approvedVersion = detail.versions.find((v) => v.approved) || null
  // Editable only while writing this revision; once it's submitted for review it's frozen.
  const editable = canEdit && detail.status === 'reporting'
  const locked = isReviewStage(detail.status)
  const staleResult = editable && approvedVersion && detail.report_version_id && detail.report_version_id !== approvedVersion.id
  // The review this revision answers, when it left comments to work through.
  const previous = detail.status === 'reporting' ? detail.revisions.find((r) => r.revision === detail.revision - 1) : undefined
  const showCommentsToggle = Boolean(previous && previous.comment_count > 0 && docx)

  return (
    <div className="flex h-screen bg-bm-shade">
      <Stepper screen="report" status={detail.status} reportGenerated={docx !== null} onNav={leave} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar
          onBack={() => leave('dashboard')}
          title={study.name}
          status={detail.status}
          revision={detail.revision}
          meta={docx && editable ? <span className={saveState === 'error' ? 'font-bold text-bm-danger-text' : ''}>{SAVE_LABELS[saveState]}</span> : undefined}
        >
          {showCommentsToggle && (
            <button onClick={() => setCommentsOpen((o) => !o)} className={choiceClass(commentsOpen, 'sm')}>
              💬 Review comments{openComments > 0 ? ` (${openComments} open)` : ''}
            </button>
          )}
          {docx && editable && (
            <Button variant="neutral" size="sm" onClick={() => setSetupOpen(true)}>
              Regenerate…
            </Button>
          )}
          <Button size="sm" onClick={() => leave('review')}>
            {locked ? 'Go to review →' : 'Continue to review →'}
          </Button>
        </TopBar>
        {/* Behind the editor's File > Open. */}
        <input
          ref={fileInput}
          type="file"
          accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0]
            e.target.value = ''
            if (file) void upload(file)
          }}
        />

        {locked && (
          <Banner
            tone="info"
            bar
            action={
              <Button variant="secondary" size="sm" onClick={() => leave('review')}>
                Go to Review
              </Button>
            }
          >
            🔒 Revision {detail.revision} has been submitted for review, so the document is locked. To change it, start a new revision on the Review page.
          </Banner>
        )}
        {staleResult && (
          <Banner
            tone="warning"
            bar
            action={
              <Button variant="secondary" size="sm" onClick={() => setSetupOpen(true)}>
                Regenerate…
              </Button>
            }
          >
            The approved result has changed since this document was generated — regenerate it to update the results in it.
          </Banner>
        )}
        {!canEdit && !locked && (
          <Banner tone="warning" bar>
            View only — you don't have edit access to this study. Ask {study.ownerName} to add you as a collaborator, or copy it from the dashboard to make your own editable version.
          </Banner>
        )}
        {error && docx && !setupOpen && (
          <Banner tone="error" bar>
            {error}
          </Banner>
        )}
        {notice && (
          <Banner tone="info" bar onDismiss={() => setNotice(null)}>
            {notice}
          </Banner>
        )}

        <div className="flex flex-1 min-h-0">
          <div className="relative flex-1 min-w-0">
            {docx ? (
              <ReportDocxEditor
                key={docVersion}
                ref={editorRef}
                docx={docx}
                fileName={reportFileName(study.name)}
                editable={editable}
                onDownload={download}
                onEdit={editable ? onEdit : undefined}
                onSave={editable ? () => void persist() : undefined}
                onOpen={editable ? () => fileInput.current?.click() : undefined}
                onReady={setEditor}
              />
            ) : editable ? (
              <div className="h-full overflow-y-auto">
                <PageBody>
                  <ReportSetup detail={detail} initial={report} authorName={currentUser.name} regenerate={false} busy={generating} error={error} onGenerate={generate} />
                </PageBody>
              </div>
            ) : (
              <EmptyState title="No report yet">No report has been generated for this study yet.</EmptyState>
            )}

            {docx && setupOpen && (
              // Over the editor rather than instead of it, so cancelling returns to the same unsaved state.
              <div className="absolute inset-0 z-50 overflow-y-auto bg-bm-navy/35">
                <PageBody>
                  <ReportSetup
                    detail={detail}
                    initial={report}
                    authorName={currentUser.name}
                    regenerate
                    busy={generating}
                    error={error}
                    onGenerate={generate}
                    onCancel={() => {
                      setSetupOpen(false)
                      setError(null)
                    }}
                  />
                </PageBody>
              </div>
            )}
          </div>

          {previous && showCommentsToggle && commentsOpen && (
            <aside className="w-96 flex-shrink-0 flex flex-col border-l border-bm-rule bg-white">
              <PanelHeader title={`Rev ${previous.revision} review comments`} />
              <div className="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-4">
                <p className="text-xs text-bm-muted">
                  {previous.reviewer_name}’s comments on revision {previous.revision}. Click one to find its place in the document; resolve it once it’s dealt with in this revision.
                </p>
                <ReviewComments
                  key={previous.revision}
                  studyId={study.id}
                  revision={previous.revision}
                  editor={editor}
                  currentUser={currentUser}
                  canComment={false}
                  canParticipate={canEdit || previous.reviewer_email === currentUser.email}
                  reviewOpen={false}
                  onOpenCountChange={setOpenComments}
                  download={{ getDocx: currentDocx, fileName: `${reportFileName(study.name)} - Rev ${detail.revision} - with Rev ${previous.revision} comments.docx` }}
                />
              </div>
            </aside>
          )}
        </div>
      </div>
    </div>
  )
}
