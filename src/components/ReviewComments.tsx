// Review comments on a submitted report revision -- our own take on Word's comments pane,
// since docx-editor's comments are a paid add-on. The threads live in the backend
// (routers/studies.py), not in the .docx. A thread made on a selection is anchored by the
// paragraph's w14:paraId (the backend gives every paragraph one when a revision is frozen,
// see docx_anchors.py) plus the quoted text, which the free engine can scroll to
// (scrollToAnchor), mark (highlightAnchor) and search for (findMatches).
//
// Shown on the Review page for the revision in review, and beside the editor while the author
// works through them in the next revision (ReportGeneration) -- where paragraphs may have
// changed, so locating falls back to finding the quoted text.
import { type KeyboardEvent, useCallback, useEffect, useMemo, useState } from 'react'
import type { Editor } from '@docx-editor.dev/react'
import type { DocAnchor } from '@docx-editor.dev/core/contracts/editor'
import type { Identity } from '../identity'
import { errorMessage, type ApiComment, DOCX_MIME, addComment, deleteComment, docxWithComments, listComments, setCommentResolved } from '../api'
import { downloadFile } from './ReportDocxEditor'
import { Banner, Button, INPUT, LinkButton, SectionTitle } from './ui'

interface Anchor {
  paraId: string
  quote: string
}

interface Thread {
  root: ApiComment
  replies: ApiComment[]
}


function shortDate(iso: string): string {
  return new Date(iso).toLocaleString('en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
}

// What to search for: the quote's first line, since a DocAnchor's search has to match inside
// one paragraph and a selection can span several.
function searchPhrase(quote: string): string {
  return (
    quote
      .split('\n')
      .map((line) => line.trim())
      .find(Boolean)
      ?.slice(0, 200) ?? ''
  )
}

// Scrolls the document to a thread's text and marks it; false when the text isn't there any more.
function locateComment(editor: Editor, comment: ApiComment): boolean {
  const search = searchPhrase(comment.quote)
  const matches = search ? editor.findMatches(search, { matchCase: true }) : []
  if (comment.para_id) {
    const anchors: DocAnchor[] = [...(search ? [{ paraId: comment.para_id, search }] : []), { paraId: comment.para_id }]
    if (anchors.some((anchor) => editor.scrollToAnchor(anchor, { block: 'center' }))) {
      editor.highlightAnchor({ paraId: comment.para_id }, { timeoutMs: 2500 })
      // Also select the exact words, when that's unambiguous.
      if (matches.length === 1) editor.selectMatch(matches[0])
      return true
    }
  }
  // The paragraph is gone (edited in a later revision) -- look for the quoted text instead.
  if (matches.length > 0) {
    editor.selectMatch(matches[0])
    return true
  }
  return false
}

// The current text selection as a comment anchor, or null when nothing (usable) is selected.
function useSelectionAnchor(editor: Editor | null, enabled: boolean): Anchor | null {
  const [anchor, setAnchor] = useState<Anchor | null>(null)
  useEffect(() => {
    setAnchor(null)
    if (!editor || !enabled) return
    return editor.on('selectionChange', (snapshot) => {
      const from = snapshot.selection?.from
      if (snapshot.selectionCollapsed || !from || !('paraId' in from)) return setAnchor(null)
      const quote = editor.query({ type: 'selectedText' }).trim()
      setAnchor(quote ? { paraId: from.paraId, quote: quote.slice(0, 1000) } : null)
    })
  }, [editor, enabled])
  return anchor
}

interface ReviewCommentsProps {
  studyId: string
  revision: number
  // The document's engine (ReportDocxEditor's onReady) -- for the selection and for locating.
  editor: Editor | null
  currentUser: Identity
  // New threads: the revision is in review and you're taking part in it.
  canComment: boolean
  // Replying and resolving: the reviewer, or anyone who can edit the study.
  canParticipate: boolean
  // Taking back your own comment only works while the review is open.
  reviewOpen: boolean
  onOpenCountChange?: (open: number) => void
  onThreadCountChange?: (threads: number) => void
  // "Download for Word, with comments": the document on screen (the frozen revision, or the
  // next revision's draft -- saved first) and the name to download it as.
  download?: { getDocx: () => Promise<Uint8Array<ArrayBuffer>>; fileName: string }
}

export default function ReviewComments({
  studyId,
  revision,
  editor,
  currentUser,
  canComment,
  canParticipate,
  reviewOpen,
  onOpenCountChange,
  onThreadCountChange,
  download,
}: ReviewCommentsProps) {
  const [comments, setComments] = useState<ApiComment[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState<string | null>(null)
  const [draft, setDraft] = useState<{ anchor: Anchor | null; text: string } | null>(null)
  const [reply, setReply] = useState<{ threadId: string; text: string } | null>(null)
  const [showResolved, setShowResolved] = useState(false)
  const [activeId, setActiveId] = useState<string | null>(null)
  const [missing, setMissing] = useState<ReadonlySet<string>>(new Set())
  const selection = useSelectionAnchor(editor, canComment)

  useEffect(() => {
    setComments(null)
    listComments(studyId, revision)
      .then(({ comments }) => setComments(comments))
      .catch((err) => setError(errorMessage(err, 'Could not load the comments')))
  }, [studyId, revision])

  // Paragraph positions, to list threads in document order like Word does.
  const paragraphOrder = useMemo(() => {
    const order = new Map<string, number>()
    editor?.query({ type: 'paragraphs' }).forEach((p, i) => p.paraId && order.set(p.paraId.toUpperCase(), i))
    return order
  }, [editor])

  const threads = useMemo<Thread[]>(() => {
    const all = comments ?? []
    const position = (c: ApiComment) => (c.para_id ? (paragraphOrder.get(c.para_id) ?? Number.MAX_SAFE_INTEGER) : -1)
    return all
      .filter((c) => !c.parent_id)
      .map((root) => ({ root, replies: all.filter((c) => c.parent_id === root.id) }))
      .sort((a, b) => position(a.root) - position(b.root) || a.root.created_at.localeCompare(b.root.created_at))
  }, [comments, paragraphOrder])

  const openCount = threads.filter((t) => !t.root.resolved_at).length
  const resolvedCount = threads.length - openCount
  useEffect(() => {
    if (!comments) return
    onOpenCountChange?.(openCount)
    onThreadCountChange?.(threads.length)
  }, [comments, openCount, threads.length, onOpenCountChange, onThreadCountChange])

  const run = async (label: string, action: () => Promise<void>) => {
    setBusy(label)
    setError(null)
    try {
      await action()
    } catch (err) {
      setError(errorMessage(err, 'That didn’t work'))
    } finally {
      setBusy(null)
    }
  }

  const submitDraft = () => {
    if (!draft?.text.trim()) return
    const { anchor, text } = draft
    void run('draft', async () => {
      const created = await addComment(studyId, revision, { body: text.trim(), ...(anchor && { para_id: anchor.paraId, quote: anchor.quote }) })
      setComments((cs) => [...(cs ?? []), created])
      setDraft(null)
    })
  }

  const submitReply = () => {
    if (!reply?.text.trim()) return
    const { threadId, text } = reply
    void run(`reply-${threadId}`, async () => {
      const created = await addComment(studyId, revision, { body: text.trim(), parent_id: threadId })
      setComments((cs) => [...(cs ?? []), created])
      setReply(null)
    })
  }

  const toggleResolved = (root: ApiComment) =>
    void run(`resolve-${root.id}`, async () => {
      const updated = await setCommentResolved(studyId, root.id, !root.resolved_at)
      setComments((cs) => (cs ?? []).map((c) => (c.id === updated.id ? updated : c)))
    })

  const downloadWithComments = () => {
    if (!download) return
    void run('download', async () => {
      const annotated = await docxWithComments(studyId, revision, await download.getDocx())
      downloadFile(annotated, download.fileName, DOCX_MIME)
    })
  }

  const remove = (comment: ApiComment) => {
    if (!window.confirm('Delete this comment?')) return
    void run(`delete-${comment.id}`, async () => {
      await deleteComment(studyId, comment.id)
      setComments((cs) => (cs ?? []).filter((c) => c.id !== comment.id))
    })
  }

  const locate = useCallback(
    (root: ApiComment) => {
      setActiveId(root.id)
      if (!editor || (!root.para_id && !root.quote)) return
      const found = locateComment(editor, root)
      setMissing((m) => {
        const next = new Set(m)
        if (found) next.delete(root.id)
        else next.add(root.id)
        return next
      })
    },
    [editor]
  )

  // Ctrl/Cmd+Enter sends, like most comment boxes.
  const sendOnCtrlEnter = (send: () => void) => (e: KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault()
      send()
    }
  }

  const visible = threads.filter((t) => showResolved || !t.root.resolved_at)

  const commentLine = (c: ApiComment, canDelete: boolean) => (
    <div>
      <div className="flex items-baseline gap-2">
        <span className="text-xs font-bold text-bm-navy">{c.author_email === currentUser.email ? 'You' : c.author_name}</span>
        <span className="text-[11px] text-bm-subtle">{shortDate(c.created_at)}</span>
        {canDelete && (
          <button
            onClick={(e) => {
              e.stopPropagation()
              remove(c)
            }}
            disabled={busy !== null}
            className="ml-auto text-[11px] text-bm-subtle hover:underline disabled:opacity-40"
          >
            Delete
          </button>
        )}
      </div>
      <p className="text-sm whitespace-pre-wrap break-words mt-0.5 text-bm-ink">{c.body}</p>
    </div>
  )
  const ownDeletable = (c: ApiComment, hasReplies: boolean) => reviewOpen && !hasReplies && c.author_email === currentUser.email

  return (
    <section>
      <SectionTitle
        aside={
          resolvedCount > 0 && (
            <LinkButton onClick={() => setShowResolved((s) => !s)}>{showResolved ? 'Hide resolved' : `Show resolved (${resolvedCount})`}</LinkButton>
          )
        }
      >
        Comments
        {comments && threads.length > 0 && <span className="ml-1.5 normal-case tracking-normal font-normal text-bm-subtle">{openCount} open</span>}
      </SectionTitle>

      {error && (
        <Banner tone="error" className="mb-3">
          {error}
        </Banner>
      )}

      {download && threads.length > 0 && (
        <Button
          variant="secondary"
          className="w-full mb-3"
          onClick={downloadWithComments}
          disabled={busy !== null}
          title="The .docx with these comments in it as Word comments, to rewrite the report in Word"
        >
          {busy === 'download' ? 'Preparing…' : '⬇ Download for Word, with comments'}
        </Button>
      )}

      {canComment &&
        (draft ? (
          <div className="rounded border p-3 mb-3 border-bm-blue bg-bm-tint/40">
            {draft.anchor ? (
              <div className="flex items-start gap-2 mb-2">
                <div className="flex-1 text-xs italic line-clamp-3 pl-2 border-l-[3px] border-bm-warning-rule text-bm-muted">“{draft.anchor.quote}”</div>
                <button onClick={() => setDraft({ ...draft, anchor: null })} className="text-xs text-bm-subtle" title="Make it a general comment">
                  ✕
                </button>
              </div>
            ) : (
              <p className="text-xs mb-2 text-bm-subtle">General comment on the whole document.</p>
            )}
            <textarea
              className={INPUT}
              style={{ minHeight: 70 }}
              placeholder="Your comment"
              value={draft.text}
              onChange={(e) => setDraft({ ...draft, text: e.target.value })}
              onKeyDown={sendOnCtrlEnter(submitDraft)}
              autoFocus
            />
            <div className="flex justify-end gap-2 mt-2">
              <Button variant="neutral" size="sm" onClick={() => setDraft(null)}>
                Cancel
              </Button>
              <Button size="sm" onClick={submitDraft} disabled={busy !== null || !draft.text.trim()}>
                {busy === 'draft' ? 'Saving…' : 'Comment'}
              </Button>
            </div>
          </div>
        ) : (
          <div className="mb-3">
            <Button
              variant="outline"
              className="w-full justify-start!"
              // Keeps the focus -- and so the selection -- in the document while clicking.
              onMouseDown={(e) => e.preventDefault()}
              onClick={() => setDraft({ anchor: selection, text: '' })}
            >
              <span className="truncate">{selection ? `+ Comment on “${searchPhrase(selection.quote)}”` : '+ General comment'}</span>
            </Button>
            {!selection && <p className="text-xs mt-1.5 text-bm-subtle">Select text in the document to comment on it.</p>}
          </div>
        ))}

      {!comments && !error && <p className="text-xs text-bm-subtle">Loading comments…</p>}
      {comments && threads.length === 0 && !canComment && <p className="text-xs text-bm-subtle">No comments on this revision.</p>}
      {comments && threads.length > 0 && visible.length === 0 && <p className="text-xs text-bm-subtle">All comments are resolved.</p>}

      <div className="flex flex-col gap-2">
        {visible.map(({ root, replies }) => {
          const resolved = Boolean(root.resolved_at)
          const anchored = Boolean(root.para_id || root.quote)
          return (
            <div
              key={root.id}
              onClick={() => locate(root)}
              className={`rounded border px-3 py-2.5 transition-colors ${anchored ? 'cursor-pointer hover:border-bm-blue' : ''} ${activeId === root.id ? 'border-bm-blue' : 'border-bm-rule-light'} ${resolved ? 'bg-bm-shade/60 opacity-75' : 'bg-white'}`}
            >
              {root.quote && (
                <div className={`text-xs italic mb-1.5 pl-2 line-clamp-2 border-l-[3px] text-bm-muted ${resolved ? 'border-bm-rule' : 'border-bm-warning-rule'}`}>
                  “{root.quote}”
                </div>
              )}
              {missing.has(root.id) && <p className="text-[11px] mb-1.5 text-bm-danger-text">This text isn’t in the document any more.</p>}
              {commentLine(root, ownDeletable(root, replies.length > 0))}
              {replies.map((r) => (
                <div key={r.id} className="mt-2 pl-3 border-l-2 border-bm-rule-light">
                  {commentLine(r, ownDeletable(r, false))}
                </div>
              ))}
              {resolved && <p className="text-[11px] mt-2 text-bm-success">✓ Resolved by {root.resolved_by_name}</p>}

              {canParticipate &&
                (reply?.threadId === root.id ? (
                  <div className="mt-2" onClick={(e) => e.stopPropagation()}>
                    <textarea
                      className={INPUT}
                      style={{ minHeight: 54 }}
                      placeholder="Reply"
                      value={reply.text}
                      onChange={(e) => setReply({ ...reply, text: e.target.value })}
                      onKeyDown={sendOnCtrlEnter(submitReply)}
                      autoFocus
                    />
                    <div className="flex justify-end gap-2 mt-1.5">
                      <Button variant="neutral" size="sm" onClick={() => setReply(null)}>
                        Cancel
                      </Button>
                      <Button size="sm" onClick={submitReply} disabled={busy !== null || !reply.text.trim()}>
                        {busy === `reply-${root.id}` ? 'Saving…' : 'Reply'}
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="flex gap-3 mt-2" onClick={(e) => e.stopPropagation()}>
                    <LinkButton onClick={() => setReply({ threadId: root.id, text: '' })}>Reply</LinkButton>
                    <LinkButton onClick={() => toggleResolved(root)} disabled={busy !== null} className={resolved ? 'text-bm-muted!' : 'text-bm-success!'}>
                      {busy === `resolve-${root.id}` ? '…' : resolved ? 'Reopen' : '✓ Resolve'}
                    </LinkButton>
                  </div>
                ))}
            </div>
          )
        })}
      </div>
    </section>
  )
}
