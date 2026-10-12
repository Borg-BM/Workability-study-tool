// "4. Review" from the Stepper flow: the current report revision goes to a reviewer -- a
// different engineer, picked from the Authentik reviewer group (or, when none is configured,
// added by email and name like sharing) -- who becomes the document's Check and approves it
// or asks for changes. A submitted revision is frozen; any further
// change starts the next revision, so every submitted revision stays available below. While
// it's in review, comments go on the document itself (ReviewComments); the author then works
// through them beside the editor in the next revision.
import { useCallback, useEffect, useState } from 'react'
import type { Editor } from '@docx-editor.dev/react'
import { canEditStudy, fromApi, type Study, type Screen } from '../App'
import type { Identity } from '../identity'
import Stepper from '../components/Stepper'
import ReportDocxEditor, { downloadFile, reportFileName } from '../components/ReportDocxEditor'
import ReviewComments from '../components/ReviewComments'
import { Banner, Button, EmptyState, Field, INPUT, PanelHeader, ScreenMessage, SectionTitle, TopBar } from '../components/ui'
import {
  errorMessage,
  DOCX_MIME,
  type ApiReview,
  type ApiReviewer,
  type ApiStudyDetail,
  changeReviewer,
  convertDocxToPdf,
  decideReview,
  docxWithComments,
  getReportDocx,
  getRevisionDocx,
  getStudyWithReport,
  listReviewers,
  startRevision,
  submitForReview,
} from '../api'


function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const OUTCOME: Record<ApiReview['status'], { label: string; className: string }> = {
  in_review: { label: 'In review', className: 'text-bm-warning' },
  approved: { label: 'Approved', className: 'text-bm-success' },
  changes_requested: { label: 'Changes requested', className: 'text-bm-danger-text' },
}

// The reviewer picker: a dropdown of the reviewer group (`reviewers`, minus the people in
// `exclude` -- you can't check your own report), or free email + name fields when no group is
// configured (`reviewers` null). `undefined` while the list loads; `error` when it couldn't be.
function ReviewerFields({
  reviewers,
  error,
  exclude,
  email,
  name,
  onEmail,
  onName,
}: {
  reviewers: ApiReviewer[] | null | undefined
  error: string | null
  exclude: string[]
  email: string
  name: string
  onEmail: (v: string) => void
  onName: (v: string) => void
}) {
  if (error) return <Banner tone="error" className="mb-4">{error}</Banner>
  if (reviewers === undefined) return <p className="text-xs mb-4 text-bm-subtle">Loading the reviewer list…</p>
  if (reviewers) {
    const options = reviewers.filter((r) => !exclude.includes(r.email))
    return (
      <div className="mb-4">
        <Field label="Reviewer" hint={options.length === 0 ? 'No one else is in the reviewer group — ask the Authentik admin to add a reviewer.' : 'Only members of the reviewer group can check reports.'}>
          <select
            className={INPUT}
            value={options.some((r) => r.email === email) ? email : ''}
            onChange={(e) => {
              const picked = options.find((r) => r.email === e.target.value)
              onEmail(picked?.email ?? '')
              onName(picked?.name ?? '')
            }}
            disabled={options.length === 0}
          >
            <option value="">Choose a reviewer…</option>
            {options.map((r) => (
              <option key={r.email} value={r.email}>
                {r.name}
              </option>
            ))}
          </select>
        </Field>
      </div>
    )
  }
  return (
    <div className="flex flex-col gap-3 mb-4">
      <Field label="Reviewer email">
        <input className={INPUT} type="email" placeholder="colleague@barge-master.com" value={email} onChange={(e) => onEmail(e.target.value)} />
      </Field>
      <Field label="Reviewer name">
        <input className={INPUT} placeholder="J. Doe" value={name} onChange={(e) => onName(e.target.value)} />
      </Field>
    </div>
  )
}

export default function Review({ study, onNav, currentUser, isAdmin }: { study: Study | null; onNav: (s: Screen, study?: Study) => void; currentUser: Identity; isAdmin: boolean }) {
  const [detail, setDetail] = useState<ApiStudyDetail | null>(null)
  const [docx, setDocx] = useState<Uint8Array<ArrayBuffer> | null>(null)
  // Bumped to remount the viewer when the document changed underneath it (e.g. Check filled in).
  const [docVersion, setDocVersion] = useState(0)
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reviewerEmail, setReviewerEmail] = useState('')
  const [reviewerName, setReviewerName] = useState('')
  // The reviewer group's members; null when no group is configured (anyone can be entered),
  // undefined while loading. A list that can't be loaded blocks submitting -- the backend
  // enforces the group either way.
  const [reviewers, setReviewers] = useState<ApiReviewer[] | null | undefined>(undefined)
  const [reviewersError, setReviewersError] = useState<string | null>(null)
  const [comment, setComment] = useState('')
  const [reassigning, setReassigning] = useState(false)
  const [editor, setEditor] = useState<Editor | null>(null)
  // Comment threads on this revision (all, and still open), as ReviewComments last counted them.
  const [commentThreads, setCommentThreads] = useState(0)
  const [openComments, setOpenComments] = useState(0)

  useEffect(() => {
    if (!study) return
    getStudyWithReport(study.id)
      .then(([s, bytes]) => {
        setDetail(s)
        setDocx(bytes)
      })
      .catch((err) => setError(errorMessage(err, 'Could not load this study')))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [study?.id])

  useEffect(() => {
    listReviewers()
      .then(({ restricted, reviewers }) => setReviewers(restricted ? reviewers : null))
      .catch((err) => setReviewersError(errorMessage(err, 'Could not load the reviewer list')))
  }, [])

  const fileName = study ? reportFileName(study.name) : 'Workability report'

  const downloadDocx = useCallback(() => {
    if (docx) downloadFile(docx, `${fileName}.docx`, DOCX_MIME)
  }, [docx, fileName])

  if (!study || !detail) {
    return (
      <div className="flex h-screen bg-bm-shade">
        <Stepper screen="review" status={study?.status ?? 'reporting'} onNav={onNav} />
        <div className="flex-1 flex flex-col min-w-0">
          {study && <TopBar onBack={() => onNav('dashboard')} title={study.name} status={study.status} />}
          <ScreenMessage error={error} />
        </div>
      </div>
    )
  }

  const canEdit = canEditStudy(fromApi(detail), currentUser, isAdmin)
  const review = detail.review
  const isReviewer = review?.reviewer_email === currentUser.email
  // The previous revision's review, while its comments are being worked through in this one.
  const previous = detail.status === 'reporting' ? detail.revisions.find((r) => r.revision === detail.revision - 1) : undefined

  // Runs one action at a time, keeping App's copy of the study in step with the result.
  const run = async (label: string, action: () => Promise<ApiStudyDetail>, { reloadDocument = false } = {}) => {
    setBusy(label)
    setError(null)
    try {
      const updated = await action()
      setDetail(updated)
      if (reloadDocument) {
        setDocx(await getReportDocx(study.id))
        setDocVersion((v) => v + 1)
      }
      onNav('review', fromApi(updated))
      return updated
    } catch (err) {
      setError(errorMessage(err, 'That didn’t work'))
      return null
    } finally {
      setBusy(null)
    }
  }

  const missingReviewer = reviewers === null ? 'Enter the reviewer’s email and name.' : 'Choose a reviewer.'

  const submit = () => {
    if (!reviewerEmail.trim() || !reviewerName.trim()) return setError(missingReviewer)
    if (!window.confirm(`Submit revision ${detail.revision} to ${reviewerName.trim()} for review? The document and the study are locked from then on; changes need a new revision.`)) return
    void run('submit', () => submitForReview(study.id, reviewerEmail.trim(), reviewerName.trim()), { reloadDocument: true })
  }

  const reassign = async () => {
    if (!reviewerEmail.trim() || !reviewerName.trim()) return setError(missingReviewer)
    if (await run('reassign', () => changeReviewer(study.id, reviewerEmail.trim(), reviewerName.trim()), { reloadDocument: true })) setReassigning(false)
  }

  const startReassigning = () => {
    setReviewerEmail('')
    setReviewerName('')
    setReassigning(true)
  }

  const decide = (decision: 'approve' | 'changes') => {
    if (decision === 'changes' && !comment.trim() && openComments === 0) return setError('Describe the changes you’re asking for, or comment on the document.')
    const commentCount = openComments === 1 ? '1 open comment' : `${openComments} open comments`
    const question =
      decision === 'approve'
        ? `Approve revision ${detail.revision}?${openComments ? ` It still has ${commentCount}.` : ''}`
        : `Send revision ${detail.revision} back${openComments ? ` with your ${commentCount}` : ' with your comments'}?`
    if (!window.confirm(question)) return
    void run(decision, () => decideReview(study.id, decision, comment.trim()))
  }

  const newRevision = async () => {
    const next = detail.revision + 1
    if (!window.confirm(`Start revision ${next}? It starts as a copy of revision ${detail.revision}, opened for editing — with its Ref. bumped to Rev ${next} and you as Author.`)) return
    const updated = await run('revision', () => startRevision(study.id))
    if (updated) onNav('report', fromApi(updated))
  }

  const downloadPdf = async (source: () => Promise<Uint8Array<ArrayBuffer>>, name: string, label: string) => {
    setBusy(label)
    setError(null)
    try {
      downloadFile(await convertDocxToPdf(await source()), `${name}.pdf`, 'application/pdf')
    } catch (err) {
      setError(errorMessage(err, 'Could not create the PDF'))
    } finally {
      setBusy(null)
    }
  }

  const downloadRevisionDocx = async (revision: number) => {
    try {
      downloadFile(await getRevisionDocx(study.id, revision), `${fileName} - Rev ${revision}.docx`, DOCX_MIME)
    } catch (err) {
      setError(errorMessage(err, 'Could not download that revision'))
    }
  }

  // A submitted revision as reviewed: its document with its comment threads as Word comments.
  const downloadRevisionWithComments = async (revision: number) => {
    setBusy(`comments-${revision}`)
    setError(null)
    try {
      const annotated = await docxWithComments(study.id, revision, await getRevisionDocx(study.id, revision))
      downloadFile(annotated, `${fileName} - Rev ${revision} - with comments.docx`, DOCX_MIME)
    } catch (err) {
      setError(errorMessage(err, 'Could not download that revision with its comments'))
    } finally {
      setBusy(null)
    }
  }

  return (
    <div className="flex h-screen bg-bm-shade">
      <Stepper screen="review" status={detail.status} reportGenerated={docx !== null} onNav={onNav} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar onBack={() => onNav('dashboard')} title={study.name} status={detail.status} revision={detail.revision}>
          <Button variant="secondary" size="sm" onClick={() => onNav('report')}>
            {detail.status === 'reporting' && canEdit ? '← Edit report' : '← Report'}
          </Button>
        </TopBar>

        <div className="flex flex-1 min-h-0">
          <div className="flex-1 min-w-0">
            {docx ? (
              <ReportDocxEditor key={docVersion} docx={docx} fileName={fileName} editable={false} onDownload={downloadDocx} onReady={setEditor} />
            ) : (
              <EmptyState title="No report document yet" action={<Button onClick={() => onNav('report')}>Generate the report</Button>}>
                Generate the report document first, then submit it here for review.
              </EmptyState>
            )}
          </div>

          <aside className="w-96 flex-shrink-0 flex flex-col border-l border-bm-rule bg-white">
            <PanelHeader title={`Review — revision ${detail.revision}`} />

            <div className="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-6">
              {error && <Banner tone="error">{error}</Banner>}

              {/* Where this revision stands, and what you can do about it */}
              <section className="flex flex-col gap-4 empty:hidden">
                {previous && previous.open_comment_count > 0 && (
                  <Banner tone="warning">
                    {previous.open_comment_count === 1 ? '1 comment' : `${previous.open_comment_count} comments`} from revision {previous.revision}’s review{' '}
                    {previous.open_comment_count === 1 ? 'is still open — it’s' : 'are still open — they’re'} beside the document on the{' '}
                    <button onClick={() => onNav('report')} className="font-bold underline">
                      Report
                    </button>{' '}
                    page.
                  </Banner>
                )}
                {detail.status === 'reporting' &&
                  (!docx ? (
                    <p className="text-sm text-bm-muted">Generate the report document first, then submit it here for review.</p>
                  ) : canEdit ? (
                    <div>
                      <SectionTitle hint={<>A different engineer checks the report — they become its <strong>Check</strong>, and it shows up on their dashboard. Submitting locks revision {detail.revision}; after that, changes need a new revision.</>}>
                        Submit for review
                      </SectionTitle>
                      <ReviewerFields
                        reviewers={reviewers}
                        error={reviewersError}
                        exclude={[currentUser.email.toLowerCase()]}
                        email={reviewerEmail}
                        name={reviewerName}
                        onEmail={setReviewerEmail}
                        onName={setReviewerName}
                      />
                      <Button className="w-full" onClick={submit} disabled={busy !== null}>
                        {busy === 'submit' ? 'Submitting…' : `Submit revision ${detail.revision} for review`}
                      </Button>
                    </div>
                  ) : (
                    <p className="text-sm text-bm-muted">Revision {detail.revision} hasn't been submitted for review yet.</p>
                  ))}

                {review && detail.status === 'in_review' && (
                  <>
                    <Banner tone="warning" title={isReviewer ? 'Waiting for your review' : `Waiting for review by ${review.reviewer_name}`}>
                      Submitted by {review.author_name} on {formatDate(review.submitted_at)}
                      {isReviewer ? '' : ` · ${review.reviewer_email}`}
                    </Banner>
                    {isReviewer ? (
                      <div className="flex flex-col gap-2">
                        <p className="text-xs text-bm-muted">Select text in the document to comment on it (your comments are listed below), then approve or ask for changes:</p>
                        <Field label="Summary for the author" className="mb-1">
                          <textarea
                            className={INPUT}
                            style={{ minHeight: 70 }}
                            placeholder={openComments ? 'Optional' : 'Optional when approving; when asking for changes, describe them here or comment on the document'}
                            value={comment}
                            onChange={(e) => setComment(e.target.value)}
                          />
                        </Field>
                        <Button variant="success" className="w-full" onClick={() => decide('approve')} disabled={busy !== null}>
                          {busy === 'approve' ? 'Approving…' : '✓ Approve'}
                        </Button>
                        <Button variant="danger" className="w-full" onClick={() => decide('changes')} disabled={busy !== null}>
                          {busy === 'changes' ? 'Sending…' : 'Request changes'}
                        </Button>
                      </div>
                    ) : (
                      canEdit &&
                      (reassigning ? (
                        <div>
                          <ReviewerFields
                            reviewers={reviewers}
                            error={reviewersError}
                            exclude={[review.author_email, review.reviewer_email, currentUser.email].map((e) => e.toLowerCase())}
                            email={reviewerEmail}
                            name={reviewerName}
                            onEmail={setReviewerEmail}
                            onName={setReviewerName}
                          />
                          <div className="flex gap-2">
                            <Button variant="neutral" className="flex-1" onClick={() => setReassigning(false)}>
                              Cancel
                            </Button>
                            <Button className="flex-1" onClick={reassign} disabled={busy !== null}>
                              {busy === 'reassign' ? 'Saving…' : 'Change reviewer'}
                            </Button>
                          </div>
                        </div>
                      ) : (
                        <Button variant="secondary" size="sm" className="self-start" onClick={startReassigning}>
                          Change reviewer
                        </Button>
                      ))
                    )}
                  </>
                )}

                {review && (detail.status === 'approved' || detail.status === 'changes_requested') && (
                  <>
                    <Banner
                      tone={detail.status === 'approved' ? 'success' : 'error'}
                      title={`${detail.status === 'approved' ? '✓ Approved' : 'Changes requested'} by ${review.reviewer_name}`}
                    >
                      {review.decided_at && formatDate(review.decided_at)}
                      {review.comment && <p className="mt-2 italic whitespace-pre-wrap text-bm-ink">"{review.comment}"</p>}
                    </Banner>
                    {canEdit && (
                      <div>
                        <Button variant="dark" className="w-full" onClick={newRevision} disabled={busy !== null}>
                          {busy === 'revision' ? 'Starting…' : `Start revision ${detail.revision + 1}`}
                        </Button>
                        <p className="text-xs mt-2 text-bm-subtle">
                          {detail.status === 'approved'
                            ? `Revision ${detail.revision} stays as approved; the new revision is where any further changes go.`
                            : `Make the requested changes in a new revision — revision ${detail.revision} stays on record as reviewed.`}
                        </p>
                      </div>
                    )}
                  </>
                )}
              </section>

              {/* Comments on this revision's document */}
              {review && (
                <ReviewComments
                  key={detail.revision}
                  studyId={study.id}
                  revision={detail.revision}
                  editor={editor}
                  currentUser={currentUser}
                  canComment={detail.status === 'in_review' && (isReviewer || canEdit)}
                  canParticipate={isReviewer || canEdit}
                  reviewOpen={detail.status === 'in_review'}
                  onOpenCountChange={setOpenComments}
                  onThreadCountChange={setCommentThreads}
                />
              )}

              {/* Downloads of this revision -- the one place for them; older revisions are under Revision history */}
              {docx && (
                <section>
                  <SectionTitle hint="Also in the document's File menu (Download .docx, Export › PDF).">Download</SectionTitle>
                  <div className="grid grid-cols-2 gap-2">
                    <Button variant="secondary" onClick={downloadDocx}>
                      ⬇ Word (.docx)
                    </Button>
                    <Button variant="secondary" onClick={() => downloadPdf(async () => docx, fileName, 'pdf')} disabled={busy === 'pdf'}>
                      {busy === 'pdf' ? 'Creating…' : '⬇ PDF'}
                    </Button>
                    {review && commentThreads > 0 && (
                      <Button
                        variant="secondary"
                        className="col-span-2"
                        onClick={() => downloadRevisionWithComments(detail.revision)}
                        disabled={busy === `comments-${detail.revision}`}
                        title="The .docx with this revision's review comments in it as Word comments, to rewrite the report in Word"
                      >
                        {busy === `comments-${detail.revision}` ? 'Preparing…' : '⬇ Word, with the review comments'}
                      </Button>
                    )}
                  </div>
                </section>
              )}

              {/* Every submitted revision */}
              {detail.revisions.length > 0 && (
                <section>
                  <SectionTitle>Revision history</SectionTitle>
                  <div className="flex flex-col gap-2">
                    {[...detail.revisions].reverse().map((r) => (
                      <div key={r.revision} className="px-3 py-2.5 rounded border border-bm-rule-light bg-bm-shade/60">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-bold text-bm-navy">Rev {r.revision}</span>
                          <span className={`text-xs font-bold ${OUTCOME[r.status].className}`}>
                            {OUTCOME[r.status].label}
                          </span>
                        </div>
                        <p className="text-xs text-bm-muted">
                          {r.author_name} → {r.reviewer_name} · {formatDate(r.decided_at ?? r.submitted_at)}
                        </p>
                        {r.comment && <p className="text-xs mt-1 italic whitespace-pre-wrap text-bm-ink">"{r.comment}"</p>}
                        {r.comment_count > 0 && (
                          <p className="text-xs mt-1 text-bm-muted">
                            💬 {r.comment_count === 1 ? '1 comment' : `${r.comment_count} comments`}
                            {r.open_comment_count > 0 ? `, ${r.open_comment_count} open` : ', all resolved'}
                          </p>
                        )}
                        {/* This revision itself is downloaded from the Download section above. */}
                        {!(docx && r.revision === detail.revision) && (
                          <div className="flex flex-wrap gap-1.5 mt-2">
                            <Button variant="outline" size="sm" onClick={() => downloadRevisionDocx(r.revision)}>
                              ⬇ .docx
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => downloadPdf(() => getRevisionDocx(study.id, r.revision), `${fileName} - Rev ${r.revision}`, `pdf-${r.revision}`)}
                              disabled={busy === `pdf-${r.revision}`}
                            >
                              {busy === `pdf-${r.revision}` ? 'Creating PDF…' : '⬇ PDF'}
                            </Button>
                            {r.comment_count > 0 && (
                              <Button variant="outline" size="sm" onClick={() => downloadRevisionWithComments(r.revision)} disabled={busy === `comments-${r.revision}`}>
                                {busy === `comments-${r.revision}` ? 'Preparing…' : '⬇ .docx + comments'}
                              </Button>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </section>
              )}
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}
