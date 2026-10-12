// "2. Upload supporting material" from the Stepper flow -- real photos, deck drawings and
// reference documents attached to the study (POST/PATCH/DELETE .../files, see
// routers/studies.py). ReportGeneration.tsx later picks specific ones by id to fill the
// report's figure slots (concept drawing, axis convention diagram, appendix images), so
// what's uploaded here is exactly the pool that screen draws from.
import { type DragEvent, useEffect, useRef, useState } from 'react'
import { canEditStudy, isReviewStage, type Study, type Screen } from '../App'
import type { Identity } from '../identity'
import Stepper from '../components/Stepper'
import { Banner, Button, EmptyState, INPUT, PanelHeader, SectionTitle, TopBar } from '../components/ui'
import { API_BASE, errorMessage, type ApiStudyFile, deleteStudyFile, getStudy, updateStudyFile, uploadStudyFile } from '../api'

export default function UploadMaterial({ study, onNav, currentUser, isAdmin }: { study: Study | null; onNav: (s: Screen) => void; currentUser: Identity; isAdmin: boolean }) {
  const [status, setStatus] = useState(study?.status ?? 'draft')
  const [hasReport, setHasReport] = useState(false)
  // The material feeds the report, so it's frozen along with it once a revision is submitted.
  const locked = isReviewStage(status)
  const canEdit = Boolean(study && canEditStudy(study, currentUser, isAdmin)) && !locked
  const [files, setFiles] = useState<ApiStudyFile[]>([])
  // The file shown in the side panel.
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [dragOver, setDragOver] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (!study) return
    getStudy(study.id)
      .then((s) => {
        setFiles(s.files)
        setSelectedId(s.files[0]?.id ?? null)
        setStatus(s.status)
        setHasReport(s.has_report_docx)
      })
      .catch(() => {})
  }, [study?.id])

  const addFiles = async (fileList: FileList | null) => {
    if (!study || !fileList || fileList.length === 0) return
    setUploading(true)
    setError(null)
    try {
      for (const file of Array.from(fileList)) {
        const uploaded = await uploadStudyFile(study.id, file)
        setFiles((fs) => [...fs, uploaded])
        setSelectedId(uploaded.id)
      }
    } catch (err) {
      setError(errorMessage(err, 'Upload failed'))
    } finally {
      setUploading(false)
    }
  }

  const updateCaption = (id: string, caption: string) => {
    setFiles((fs) => fs.map((f) => (f.id === id ? { ...f, caption } : f)))
  }

  // Only persists on blur (not every keystroke) -- one PATCH per edit, not one per character.
  const commitCaption = (id: string) => {
    if (!study) return
    const f = files.find((f) => f.id === id)
    if (f) updateStudyFile(study.id, id, { caption: f.caption }).catch(() => {})
  }

  const removeFile = (id: string) => {
    if (!study) return
    const index = files.findIndex((f) => f.id === id)
    const rest = files.filter((f) => f.id !== id)
    setFiles(rest)
    // Keep a file selected: the one that took its place, else the one before it.
    setSelectedId(rest[Math.min(index, rest.length - 1)]?.id ?? null)
    deleteStudyFile(study.id, id).catch(() => {})
  }

  // Swaps two files' sort_order both locally and on the server -- each move is its own
  // pair of PATCHes rather than re-sending the whole list.
  const swap = (i: number, j: number) => {
    if (!study || j < 0 || j >= files.length) return
    const a = files[i]
    const b = files[j]
    setFiles((fs) => {
      const next = [...fs]
      ;[next[i], next[j]] = [next[j], next[i]]
      return next
    })
    updateStudyFile(study.id, a.id, { sort_order: b.sort_order }).catch(() => {})
    updateStudyFile(study.id, b.id, { sort_order: a.sort_order }).catch(() => {})
  }

  const selectedIndex = files.findIndex((f) => f.id === selectedId)
  const selected = selectedIndex >= 0 ? files[selectedIndex] : null

  // The whole work area takes dropped files, like a document takes edits on the report page.
  const dropTarget = canEdit
    ? {
        onDragOver: (e: DragEvent) => {
          e.preventDefault()
          setDragOver(true)
        },
        onDragLeave: (e: DragEvent) => {
          if (!e.currentTarget.contains(e.relatedTarget as Node | null)) setDragOver(false)
        },
        onDrop: (e: DragEvent) => {
          e.preventDefault()
          setDragOver(false)
          void addFiles(e.dataTransfer.files)
        },
      }
    : {}

  return (
    <div className="flex h-screen bg-bm-shade">
      <Stepper screen="upload" status={status} reportGenerated={hasReport} onNav={onNav} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar
          onBack={() => onNav('dashboard')}
          title={study?.name || 'Study'}
          status={status}
          revision={study?.revision}
          meta={uploading ? 'Uploading…' : files.length === 1 ? '1 file' : `${files.length} files`}
        >
          <Button size="sm" onClick={() => onNav('report')}>
            {locked ? 'Go to the report →' : 'Continue to report generation →'}
          </Button>
        </TopBar>
        <input ref={inputRef} type="file" multiple accept={ACCEPT} className="hidden" onChange={(e) => void addFiles(e.target.files)} />

        {locked && (
          <Banner tone="info" bar>
            🔒 Revision {study?.revision} of the report has been submitted for review, so its material is locked. Changes need a new revision, started from the Review page.
          </Banner>
        )}
        {!locked && !canEdit && (
          <Banner tone="warning" bar>
            View only — you don't have edit access to this study. Ask {study?.ownerName} to add you as a collaborator, or copy it from the dashboard to make your own editable version.
          </Banner>
        )}
        {error && (
          <Banner tone="error" bar onDismiss={() => setError(null)}>
            {error}
          </Banner>
        )}

        <div className="flex flex-1 min-h-0">
          {/* Work area: the material itself */}
          <main {...dropTarget} className={`relative flex-1 min-w-0 overflow-y-auto transition-colors ${dragOver ? 'bg-bm-tint' : ''}`}>
            {files.length === 0 ? (
              <div className="h-full p-8">
                {canEdit ? (
                  <button
                    onClick={() => inputRef.current?.click()}
                    className={`w-full h-full rounded border-2 border-dashed bg-white transition-colors ${dragOver ? 'border-bm-blue' : 'border-bm-rule hover:border-bm-blue'}`}
                  >
                    <EmptyState icon="↑" title={uploading ? 'Uploading…' : 'Drag files here or click to browse'}>
                      Deck drawings, photographs and reference documents for the report — images can fill its figures. {FORMATS}
                    </EmptyState>
                  </button>
                ) : (
                  <EmptyState title="No material uploaded">No supporting material was uploaded for this study.</EmptyState>
                )}
              </div>
            ) : (
              <div className="p-6 grid gap-4" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))' }}>
                {files.map((f, i) => (
                  <button
                    key={f.id}
                    onClick={() => setSelectedId(f.id)}
                    className={`text-left rounded border-2 bg-white overflow-hidden transition-colors ${f.id === selectedId ? 'border-bm-blue' : 'border-transparent hover:border-bm-rule'}`}
                  >
                    <Thumbnail file={f} className="h-40 border-b border-bm-rule-light" />
                    <div className="px-3 py-2.5">
                      <div className="flex items-baseline gap-2">
                        <span className="text-xs font-bold text-bm-subtle">{i + 1}</span>
                        <span className="text-sm font-bold truncate text-bm-ink">{f.original_filename}</span>
                      </div>
                      <div className={`text-xs truncate mt-0.5 ${f.caption ? 'text-bm-muted' : 'italic text-bm-placeholder'}`}>{f.caption || 'No caption'}</div>
                    </div>
                  </button>
                ))}
              </div>
            )}
            {dragOver && files.length > 0 && (
              <div className="pointer-events-none absolute inset-3 rounded border-2 border-dashed border-bm-blue flex items-end justify-center pb-6">
                <span className="px-3 py-1.5 rounded text-sm font-bold bg-bm-blue text-white">Drop to upload</span>
              </div>
            )}
          </main>

          {/* Side panel: the selected file */}
          <aside className="w-96 flex-shrink-0 flex flex-col border-l border-bm-rule bg-white">
            <PanelHeader title="File details" />
            <div className="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-6">
              {selected ? (
                <>
                  <section>
                    <Thumbnail file={selected} className="h-52 rounded border border-bm-rule" />
                    <div className="text-sm font-bold mt-3 break-words text-bm-ink">{selected.original_filename}</div>
                    <div className="text-xs mt-0.5 text-bm-subtle">
                      {selected.kind === 'image' ? 'Image — can fill a figure of the report' : 'Document — for reference'} · {selectedIndex + 1} of {files.length}
                    </div>
                  </section>

                  <section>
                    <SectionTitle hint="Used as the figure caption when this image goes into the report.">Caption</SectionTitle>
                    <input
                      className={INPUT}
                      placeholder="Add caption or description…"
                      value={selected.caption}
                      disabled={!canEdit}
                      onChange={(e) => updateCaption(selected.id, e.target.value)}
                      onBlur={() => commitCaption(selected.id)}
                    />
                  </section>

                  {canEdit && (
                    <section>
                      <SectionTitle>Order & removal</SectionTitle>
                      <div className="flex gap-2">
                        <Button variant="neutral" size="sm" onClick={() => swap(selectedIndex, selectedIndex - 1)} disabled={selectedIndex === 0}>
                          ↑ Move up
                        </Button>
                        <Button variant="neutral" size="sm" onClick={() => swap(selectedIndex, selectedIndex + 1)} disabled={selectedIndex === files.length - 1}>
                          ↓ Move down
                        </Button>
                        <Button
                          variant="danger"
                          size="sm"
                          className="ml-auto"
                          onClick={() => window.confirm(`Remove "${selected.original_filename}" from this study?`) && removeFile(selected.id)}
                        >
                          Remove
                        </Button>
                      </div>
                    </section>
                  )}
                </>
              ) : (
                <p className="text-sm text-bm-subtle">
                  {files.length === 0 ? 'Uploaded files show up here — select one to add a caption, reorder it or remove it.' : 'Select a file to see its details.'}
                </p>
              )}

              {canEdit && (
                <section>
                  <SectionTitle hint={FORMATS}>Add material</SectionTitle>
                  <Button variant="outline" className="w-full" onClick={() => inputRef.current?.click()} disabled={uploading}>
                    {uploading ? 'Uploading…' : '+ Add files'}
                  </Button>
                  <p className="text-xs mt-2 text-bm-subtle">Or drop files anywhere on the material.</p>
                </section>
              )}
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}

const ACCEPT = '.jpg,.jpeg,.png,.gif,.webp,.pdf,.dwg,.doc,.docx,.xls,.xlsx'
const FORMATS = 'Images (JPG, PNG, GIF, WebP) and documents (PDF, DWG, DOC, XLS).'

/** An image's picture, or a document's file type, filling a fixed-height tile. */
function Thumbnail({ file, className = '' }: { file: ApiStudyFile; className?: string }) {
  return (
    <div className={`flex items-center justify-center overflow-hidden bg-bm-shade ${className}`}>
      {file.kind === 'image' ? (
        <img src={`${API_BASE}${file.url}`} alt={file.original_filename} className="w-full h-full object-contain bg-white" />
      ) : (
        <span className="px-3 py-2 rounded border border-bm-rule bg-white text-sm font-bold tracking-wide text-bm-subtle">
          {file.original_filename.split('.').pop()?.toUpperCase() || 'FILE'}
        </span>
      )}
    </div>
  )
}
