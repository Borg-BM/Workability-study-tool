// Owner-or-admin study management, in one place: renaming the study reference, sharing
// (grant/revoke edit rights by email), archiving (hide from the main dashboard tabs without
// touching any data, fully reversible), transferring ownership (e.g. when the current owner
// leaves the company), and deleting (irreversible). Opened from StudyBuilder.tsx's top bar or
// StudiesDashboard.tsx's row actions, only for someone the backend will let do these things
// (owner or admin, see routers/studies.py's _require_owner) -- so no further gating inside.
import { useState } from 'react'
import { errorMessage, addCollaborator, archiveStudy, removeCollaborator, transferOwnership, unarchiveStudy, updateStudy } from '../api'
import { Banner, Button, INPUT, Modal, SectionTitle } from './ui'

// An input that shares its row with a button.
const ROW_INPUT = `${INPUT} flex-1 min-w-0`

interface Props {
  studyId: string
  studyName: string
  ownerName: string
  ownerEmail: string
  collaborators: string[]
  archived: boolean
  onRenamed: (name: string) => void
  onCollaboratorsChange: (collaborators: string[]) => void
  onArchivedChange: (archived: boolean) => void
  onTransferred: (newOwnerEmail: string, newOwnerName: string) => void
  onDelete: () => void
  onClose: () => void
}

export default function ManageStudyModal({
  studyId,
  studyName,
  ownerName,
  ownerEmail,
  collaborators,
  archived,
  onRenamed,
  onCollaboratorsChange,
  onArchivedChange,
  onTransferred,
  onDelete,
  onClose,
}: Props) {
  const [name, setName] = useState(studyName)
  const [email, setEmail] = useState('')
  const [transferEmail, setTransferEmail] = useState('')
  const [transferName, setTransferName] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const rename = async () => {
    const trimmed = name.trim()
    if (!trimmed || trimmed === studyName) return
    setBusy(true)
    setError(null)
    try {
      const updated = await updateStudy(studyId, { name: trimmed })
      onRenamed(updated.name)
    } catch (err) {
      setError(errorMessage(err, 'Could not rename the study'))
    } finally {
      setBusy(false)
    }
  }

  const addShare = async () => {
    const trimmed = email.trim()
    if (!trimmed) return
    setBusy(true)
    setError(null)
    try {
      const { collaborators: next } = await addCollaborator(studyId, trimmed)
      onCollaboratorsChange(next)
      setEmail('')
    } catch (err) {
      setError(errorMessage(err, 'Could not add collaborator'))
    } finally {
      setBusy(false)
    }
  }

  const removeShare = async (collaboratorEmail: string) => {
    setBusy(true)
    setError(null)
    try {
      const { collaborators: next } = await removeCollaborator(studyId, collaboratorEmail)
      onCollaboratorsChange(next)
    } catch (err) {
      setError(errorMessage(err, 'Could not remove collaborator'))
    } finally {
      setBusy(false)
    }
  }

  const transferOwner = async () => {
    const trimmed = transferEmail.trim()
    if (!trimmed) return
    if (trimmed.toLowerCase() === ownerEmail.toLowerCase()) {
      setError('That email already owns this study.')
      return
    }
    if (!confirm(`Transfer ownership of "${studyName}" from ${ownerName} to ${trimmed}? They become the owner -- able to manage sharing, archive, delete, and transfer it again.`)) return
    setBusy(true)
    setError(null)
    try {
      const updated = await transferOwnership(studyId, trimmed, transferName.trim() || undefined)
      onTransferred(updated.owner_email, updated.owner_name)
      setTransferEmail('')
      setTransferName('')
    } catch (err) {
      setError(errorMessage(err, 'Could not transfer ownership'))
    } finally {
      setBusy(false)
    }
  }

  const toggleArchived = async () => {
    setBusy(true)
    setError(null)
    try {
      await (archived ? unarchiveStudy(studyId) : archiveStudy(studyId))
      onArchivedChange(!archived)
    } catch (err) {
      setError(errorMessage(err, 'Could not update archive status'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Modal
      title={`Manage "${studyName}"`}
      width={820}
      onClose={onClose}
      footer={
        <Button variant="neutral" className="ml-auto" onClick={onClose}>
          Done
        </Button>
      }
    >
      <div className="px-6 py-5">
        {error && (
          <Banner tone="error" className="mb-4">
            {error}
          </Banner>
        )}

        <div className="grid grid-cols-2 gap-x-8">
          {/* Left column: the study's name and who can edit it */}
          <div className="flex flex-col gap-6">
            <section>
              <SectionTitle>Study reference</SectionTitle>
              <div className="flex gap-2">
                <input className={ROW_INPUT} value={name} onChange={(e) => setName(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && rename()} />
                <Button onClick={rename} disabled={busy || !name.trim() || name.trim() === studyName}>
                  Save
                </Button>
              </div>
            </section>

            <section>
              <SectionTitle hint={`Everyone at Barge Master can already see this study. People added here can also edit it, without becoming the owner (${ownerName}).`}>
                Share
              </SectionTitle>
              <div className="flex gap-2 mb-2.5">
                <input
                  className={ROW_INPUT}
                  type="email"
                  placeholder="colleague@barge-master.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && addShare()}
                />
                <Button onClick={addShare} disabled={busy || !email.trim()}>
                  Add
                </Button>
              </div>
              {collaborators.length === 0 ? (
                <p className="text-xs text-bm-subtle">No one else has edit access yet.</p>
              ) : (
                <div className="flex flex-col gap-1.5">
                  {collaborators.map((c) => (
                    <div key={c} className="flex items-center justify-between gap-2 px-3 py-1.5 rounded bg-bm-shade">
                      <span className="text-sm truncate text-bm-navy">{c}</span>
                      <Button variant="danger" size="sm" onClick={() => removeShare(c)} disabled={busy}>
                        Remove
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>

          {/* Right column: handing it over, hiding it, or deleting it */}
          <div className="flex flex-col gap-6">
            <section>
              <SectionTitle hint={`Reassign this study, e.g. when ${ownerName} leaves the company. The new owner gets full control; you keep access only if you're listed under Share.`}>
                Transfer ownership
              </SectionTitle>
              <input
                className={`${INPUT} mb-2`}
                type="email"
                placeholder="new-owner@barge-master.com"
                value={transferEmail}
                onChange={(e) => setTransferEmail(e.target.value)}
              />
              <div className="flex gap-2">
                <input className={ROW_INPUT} type="text" placeholder="Name (optional)" value={transferName} onChange={(e) => setTransferName(e.target.value)} />
                <Button variant="secondary" onClick={transferOwner} disabled={busy || !transferEmail.trim()}>
                  Transfer
                </Button>
              </div>
            </section>

            <section>
              <SectionTitle
                hint={`${archived ? 'Archived: hidden from the main dashboard tabs. Unarchive to bring it back.' : 'Archiving hides the study from the main dashboard tabs; nothing is deleted.'} Deleting cannot be undone.`}
              >
                Archive or delete
              </SectionTitle>
              <div className="flex gap-2">
                <Button variant="secondary" className="flex-1" onClick={toggleArchived} disabled={busy}>
                  {archived ? '↩ Unarchive' : '🗄 Archive'}
                </Button>
                <Button
                  variant="danger"
                  className="flex-1"
                  onClick={() => {
                    if (confirm(`Delete study "${studyName}"? This cannot be undone.`)) onDelete()
                  }}
                  disabled={busy}
                >
                  Delete study
                </Button>
              </div>
            </section>
          </div>
        </div>
      </div>
    </Modal>
  )
}
