// Small colored pill used on the dashboard table and each screen's top bar. Purely
// presentational -- see App.tsx's StudyStatus type for what each value actually means.
import type { StudyStatus } from '../App'

const config: Record<StudyStatus, { label: string; bg: string; color: string; border: string }> = {
  draft: { label: 'Draft', bg: '#F0F0F0', color: '#666', border: '#C9C9C9' },
  in_progress: { label: 'In progress', bg: '#E6F7FD', color: '#007BB5', border: '#00ADEF' },
  reporting: { label: 'Reporting', bg: '#E6F7FD', color: '#007BB5', border: '#00ADEF' },
  in_review: { label: 'In review', bg: '#FFFBEB', color: '#92400E', border: '#F59E0B' },
  approved: { label: 'Approved ✓', bg: '#051642', color: '#fff', border: '#051642' },
  changes_requested: { label: 'Changes requested', bg: '#FEF2F2', color: '#991B1B', border: '#ef4444' },
}

export default function StatusChip({ status }: { status: StudyStatus }) {
  const c = config[status]
  return (
    <span
      className="inline-block px-2.5 py-0.5 text-xs font-bold rounded-sm whitespace-nowrap"
      style={{ background: c.bg, color: c.color, border: `1px solid ${c.border}`, letterSpacing: '0.04em' }}
    >
      {c.label.toUpperCase()}
    </span>
  )
}
