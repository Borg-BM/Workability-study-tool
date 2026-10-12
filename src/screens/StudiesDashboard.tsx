// Entry screen: tabs over the same study list -- "My Studies" (you own it), "Shared
// with me" (someone else's, but you've been granted edit rights -- see
// ManageStudyModal.tsx's sharing section), "For review" (reports waiting for you to review
// them), "All Studies" (everyone -- every study is readable by anyone, see
// backend/app/db.py's list_studies() docstring; only writes are permission-gated), and
// "Archived" (hidden from the others, see db.set_study_archived -- purely a display-state
// flag, fully reversible). Clicking a row calls `onOpen` (App.tsx's openStudy -- opens the
// study at the stage it's at).
import { useEffect, useState } from 'react'
import { awaitsReviewBy, canEditStudy, fromApi, isReviewStage, isStudyOwner, type Study } from '../App'
import type { Identity } from '../identity'
import { errorMessage, copyStudy } from '../api'
import StatusChip from '../components/StatusChip'
import ManageStudyModal from '../components/ManageStudyModal'
import { Banner, Button, EmptyState, PageTitle, TABLE_CELL, TABLE_HEAD_CELL, choiceClass } from '../components/ui'

interface Props {
  studies: Study[]
  currentUser: Identity
  isAdmin: boolean
  onOpen: (s: Study) => void
  onNew: () => void
  onDelete: (s: Study) => void
  onSignOut: () => void
  loadError?: string | null
}

type Tab = 'mine' | 'shared' | 'review' | 'all' | 'archived'

const TABS: [Tab, string][] = [
  ['mine', 'My Studies'],
  ['shared', 'Shared with me'],
  ['review', 'For review'],
  ['all', 'All Studies'],
  ['archived', 'Archived'],
]

export default function StudiesDashboard({ studies, currentUser, isAdmin, onOpen, onNew, onDelete, onSignOut, loadError }: Props) {
  const [tab, setTab] = useState<Tab>('mine')
  const [copyingId, setCopyingId] = useState<string | null>(null)
  const [copyError, setCopyError] = useState<string | null>(null)
  const [manageTarget, setManageTarget] = useState<Study | null>(null)
  // A local, patchable copy of `studies` -- Manage actions (share/archive) already know
  // their new value from the API response, so patching it here is instant feedback
  // without waiting on App.tsx's next full refetch (which only happens on nav back to
  // this screen anyway, see App.tsx's navigate()).
  const [localStudies, setLocalStudies] = useState(studies)
  useEffect(() => setLocalStudies(studies), [studies])

  const owned = localStudies.filter((s) => isStudyOwner(s, currentUser))
  const sharedWithMe = localStudies.filter((s) => !isStudyOwner(s, currentUser) && s.collaborators.includes(currentUser.email))
  const toReview = localStudies.filter((s) => awaitsReviewBy(s, currentUser))
  const byTab: Record<Tab, Study[]> = {
    mine: owned.filter((s) => !s.archived),
    shared: sharedWithMe.filter((s) => !s.archived),
    review: toReview,
    all: localStudies.filter((s) => !s.archived),
    archived: localStudies.filter((s) => s.archived && (isStudyOwner(s, currentUser) || s.collaborators.includes(currentUser.email))),
  }
  const visible = byTab[tab]
  const showOwnerColumn = tab === 'all' || tab === 'archived'

  const handleCopy = async (e: React.MouseEvent, s: Study) => {
    e.stopPropagation()
    setCopyingId(s.id)
    setCopyError(null)
    try {
      const copy = await copyStudy(s.id)
      onOpen(fromApi(copy)) // jump straight into the new copy (already vessel-locked, so this lands on Build study, not Setup)
    } catch (err) {
      setCopyError(errorMessage(err, 'Could not copy this study'))
    } finally {
      setCopyingId(null)
    }
  }

  const patchStudy = (id: string, patch: Partial<Study>) =>
    setLocalStudies((ss) => ss.map((s) => (s.id === id ? { ...s, ...patch } : s)))

  return (
    <div className="min-h-screen flex flex-col bg-bm-shade">
      {/* Masthead -- the same brand mark as the study screens' sidebar */}
      <header className="h-14 flex-shrink-0 flex items-center px-8 bg-bm-navy">
        <button onClick={() => setTab('mine')} title="Back to your studies" className="flex items-center gap-3 rounded transition-colors hover:bg-white/5 -ml-2 px-2 py-1 text-left">
          <span className="w-7 h-7 rounded flex items-center justify-center bg-bm-shade">
            <img src="/favicon.png" alt="" className="w-5 h-5" />
          </span>
          <span>
            <span className="block text-[10px] font-bold uppercase tracking-widest text-bm-blue leading-tight">Barge Master</span>
            <span className="block font-bold text-white text-sm leading-tight">BM Workability Study Builder</span>
          </span>
        </button>
        <a href="/third-party-licenses.txt" target="_blank" rel="noreferrer" className="ml-auto mr-4 text-xs text-white/50 transition-colors hover:text-white/80">
          Open-source licences
        </a>
        <span className="text-xs text-white/70">
          Signed in as <strong className="text-white">{currentUser.name}</strong>
        </span>
        <button onClick={onSignOut} className="ml-3 px-3 py-1.5 text-xs font-bold rounded border border-white/40 text-white transition-colors hover:bg-white/10">
          Sign out
        </button>
      </header>

      <main className="flex-1 px-10 py-8 max-w-6xl w-full mx-auto">
        <PageTitle
          title="Studies"
          actions={
            <Button onClick={onNew}>
              <span className="text-base leading-none">+</span> New study
            </Button>
          }
        >
          {visible.length === 1 ? '1 study' : `${visible.length} studies`}
        </PageTitle>

        <div className="flex gap-2 mb-5">
          {TABS.map(([t, label]) => (
            <button key={t} onClick={() => setTab(t)} className={choiceClass(tab === t)}>
              {label}
              {t === 'review' && toReview.length > 0 && (
                <span className="px-1.5 py-0.5 rounded-full text-xs text-white leading-none bg-bm-warning-rule">{toReview.length}</span>
              )}
            </button>
          ))}
        </div>

        <div className="flex flex-col gap-3 mb-5 empty:hidden">
          {toReview.length > 0 && tab !== 'review' && (
            <Banner
              tone="warning"
              title={`${toReview.length === 1 ? '1 report is' : `${toReview.length} reports are`} waiting for your review.`}
              action={
                <Button variant="secondary" size="sm" onClick={() => setTab('review')}>
                  Show
                </Button>
              }
            />
          )}
          {loadError && (
            <Banner tone="error" title="Can't reach the backend.">
              {loadError}
            </Banner>
          )}
          {copyError && <Banner tone="error">{copyError}</Banner>}
        </div>

        {visible.length === 0 ? (
          <EmptyStudies onNew={onNew} tab={tab} />
        ) : (
          <div className="bg-white border border-bm-rule rounded overflow-hidden">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr>
                  {[...(showOwnerColumn ? ['Study ref.', 'Owner'] : ['Study ref.']), 'Vessel', 'Project', 'Status', 'Last edited', ''].map((h) => (
                    <th key={h} className={TABLE_HEAD_CELL}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {visible.map((s) => {
                  const owner = isStudyOwner(s, currentUser)
                  const canManage = owner || isAdmin
                  const canEdit = canEditStudy(s, currentUser, isAdmin)
                  return (
                    <tr key={s.id} className="cursor-pointer border-b border-bm-rule-light last:border-b-0 transition-colors hover:bg-bm-tint/50" onClick={() => onOpen(s)}>
                      <td className={`${TABLE_CELL} font-bold text-bm-navy`}>
                        {s.name}
                        {awaitsReviewBy(s, currentUser) && (
                          <span className="ml-2 px-2 py-0.5 text-xs font-bold rounded-sm whitespace-nowrap tracking-wide text-white bg-bm-warning-rule">REVIEW REQUESTED</span>
                        )}
                      </td>
                      {showOwnerColumn && (
                        <td className={`${TABLE_CELL} text-bm-muted`}>{owner ? <span className="font-bold text-bm-blue">You</span> : s.ownerName}</td>
                      )}
                      <td className={`${TABLE_CELL} text-bm-ink`}>{s.vessel}</td>
                      <td className={`${TABLE_CELL} text-bm-muted`}>{s.project}</td>
                      <td className={`${TABLE_CELL} whitespace-nowrap`}>
                        <StatusChip status={s.status} />
                        {(s.revision > 0 || isReviewStage(s.status)) && <span className="ml-2 text-xs font-bold text-bm-navy">Rev {s.revision}</span>}
                      </td>
                      <td className={`${TABLE_CELL} text-bm-subtle`}>{s.lastEdited}</td>
                      <td className={`${TABLE_CELL} text-right whitespace-nowrap`}>
                        <div className="inline-flex gap-2">
                          {!canEdit && (
                            <Button variant="outline" size="sm" onClick={(e) => handleCopy(e, s)} disabled={copyingId === s.id}>
                              {copyingId === s.id ? 'Copying…' : 'Copy to my studies'}
                            </Button>
                          )}
                          {canManage && (
                            <Button
                              variant="secondary"
                              size="sm"
                              onClick={(e) => {
                                e.stopPropagation()
                                setManageTarget(s)
                              }}
                            >
                              Manage
                            </Button>
                          )}
                          <Button
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation()
                              onOpen(s)
                            }}
                          >
                            Open →
                          </Button>
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </main>

      {manageTarget && (
        <ManageStudyModal
          studyId={manageTarget.id}
          studyName={manageTarget.name}
          ownerName={manageTarget.ownerName}
          ownerEmail={manageTarget.ownerEmail}
          collaborators={manageTarget.collaborators}
          archived={manageTarget.archived}
          onCollaboratorsChange={(collaborators) => {
            patchStudy(manageTarget.id, { collaborators })
            setManageTarget((t) => (t ? { ...t, collaborators } : t))
          }}
          onArchivedChange={(archived) => {
            patchStudy(manageTarget.id, { archived })
            setManageTarget((t) => (t ? { ...t, archived } : t))
          }}
          onRenamed={(name) => {
            patchStudy(manageTarget.id, { name })
            setManageTarget((t) => (t ? { ...t, name } : t))
          }}
          onTransferred={(ownerEmail, ownerName) => {
            patchStudy(manageTarget.id, { ownerEmail, ownerName })
            setManageTarget(null)
          }}
          onDelete={() => {
            onDelete(manageTarget)
            setManageTarget(null)
          }}
          onClose={() => setManageTarget(null)}
        />
      )}
    </div>
  )
}

function EmptyStudies({ onNew, tab }: { onNew: () => void; tab: Tab }) {
  const messages: Record<Tab, string> = {
    mine: "You don't have any studies yet",
    shared: "No one's shared a study with you yet",
    review: 'Nothing waiting for your review',
    all: 'No studies yet',
    archived: 'Nothing archived',
  }
  return (
    <div className="border-2 border-dashed border-bm-rule rounded bg-white">
      <EmptyState
        icon={<img src="/bm-logo.png" alt="Barge Master" className="w-36" />}
        title={messages[tab]}
        action={tab !== 'archived' && tab !== 'shared' && tab !== 'review' ? <Button onClick={onNew}>+ New study</Button> : undefined}
      >
        {tab === 'archived'
          ? 'Studies you archive (from their Manage panel) show up here, hidden from the main tabs until you bring them back.'
          : tab === 'review'
            ? 'When a colleague submits a report for you to check, it shows up here.'
            : 'Create your first workability study to get started. Studies guide you from RAO selection through to a reviewed report.'}
      </EmptyState>
    </div>
  )
}
