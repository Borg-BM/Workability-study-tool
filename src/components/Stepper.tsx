// The navy sidebar shown on every screen except the dashboard -- both the 4-phase
// progress list ("Build study" -> ... -> "Review") and the app's name/logo (which leads back
// to the studies list). Only phases the study has reached can be opened (earlier ones
// read-only, see each screen's lock); later ones stay greyed out until the workflow gets there.
import { isBuildStage, isReviewStage, type Screen, type StudyStatus } from '../App'

type Phase = { id: number; label: string; screen: Screen }

const PHASES: Phase[] = [
  { id: 1, label: 'Build study', screen: 'builder' },
  { id: 2, label: 'Upload material', screen: 'upload' },
  { id: 3, label: 'Generate report', screen: 'report' },
  { id: 4, label: 'Review', screen: 'review' },
]

// Building unlocks nothing further until a result is approved; from then on the report and
// its review are reachable (the Review page is where a revision gets submitted).
const furthestPhase = (status: StudyStatus) => (isBuildStage(status) ? 1 : 4)

// Material is optional, so it counts as done once you've moved past it or there's a report.
function isDone(phase: number, status: StudyStatus, current: number, reportGenerated: boolean): boolean {
  if (isBuildStage(status)) return false
  if (phase === 1) return true
  if (phase === 2) return reportGenerated || current > 2 || isReviewStage(status)
  if (phase === 3) return reportGenerated || isReviewStage(status)
  return status === 'approved'
}

export default function Stepper({
  screen,
  status,
  reportGenerated = false,
  onNav,
}: {
  screen: Screen
  status: StudyStatus
  reportGenerated?: boolean
  onNav: (s: Screen) => void
}) {
  // StudySetup isn't a phase of its own: it shows as the start of "Build study".
  const current = PHASES.find((p) => p.screen === screen)?.id ?? 1
  const furthest = furthestPhase(status)

  return (
    <nav className="sticky top-0 h-screen self-start w-52 flex-shrink-0 flex flex-col border-r overflow-y-auto" style={{ background: '#051642', borderColor: '#0a2260' }}>
      <button
        onClick={() => onNav('dashboard')}
        title="Back to all studies"
        className="px-5 py-5 border-b flex items-center gap-3 text-left transition-colors hover:bg-white/5"
        style={{ borderColor: '#0a2260' }}
      >
        {/* favicon.png's diamond mark is a near-navy (#171c3f), almost invisible on this
            sidebar's navy background -- a light backing chip keeps it visible without
            recoloring the actual logo asset. */}
        <div className="w-7 h-7 flex-shrink-0 rounded flex items-center justify-center" style={{ background: '#F5F5F3' }}>
          <img src="/favicon.png" alt="" className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-bold uppercase tracking-widest mb-1" style={{ color: '#00ADEF' }}>Barge Master</div>
          <div className="text-white font-bold text-sm leading-tight">BM Workability Study Builder</div>
        </div>
      </button>
      <div className="flex-1 py-6 px-4 flex flex-col gap-1">
        {PHASES.map((p) => {
          const reachable = p.id <= furthest
          const done = isDone(p.id, status, current, reportGenerated) // filled circle + checkmark
          const active = current === p.id // highlighted background + accent-colored label
          return (
            <button
              key={p.id}
              onClick={() => onNav(p.screen)}
              disabled={!reachable}
              title={reachable ? undefined : 'Not reached yet — finish the earlier steps first'}
              className="flex items-start gap-3 px-3 py-3 rounded text-left w-full transition-colors disabled:cursor-not-allowed"
              style={{ background: active ? 'rgba(0,173,239,0.15)' : 'transparent' }}
            >
              <div
                className="w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5"
                style={{
                  background: done || active ? '#00ADEF' : 'rgba(255,255,255,0.1)',
                  color: done || active ? '#fff' : 'rgba(255,255,255,0.4)',
                  border: done || active ? 'none' : '1px solid rgba(255,255,255,0.2)',
                  opacity: reachable ? 1 : 0.5,
                }}
              >
                {done ? '✓' : p.id}
              </div>
              <span
                className="text-sm font-medium leading-tight"
                style={{ color: active ? '#00ADEF' : done ? 'rgba(255,255,255,0.8)' : reachable ? 'rgba(255,255,255,0.6)' : 'rgba(255,255,255,0.25)' }}
              >
                {p.label}
              </span>
            </button>
          )
        })}
      </div>
      {/* Open-source attribution (Apache-2.0 etc.): the full texts are in public/third-party-licenses.txt */}
      <a href="/third-party-licenses.txt" target="_blank" rel="noreferrer" className="mt-auto px-5 py-3 text-[11px] text-white/40 transition-colors hover:text-white/70">
        Open-source licences
      </a>
    </nav>
  )
}
