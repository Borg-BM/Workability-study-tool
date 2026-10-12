// Top-level component: owns which screen is showing and which study is "active" (being
// worked on). There's no router library here -- `screen` is just a string discriminant
// and navigate() is the only way any child screen moves between them (passed down as
// `onNav`). Every screen but StudiesDashboard (the entry point / "back to list" target)
// shows the Stepper sidebar (see Stepper.tsx).
import { lazy, Suspense, useEffect, useState } from 'react'
import StudiesDashboard from './screens/StudiesDashboard'
import StudySetup from './screens/StudySetup'
import StudyBuilder from './screens/StudyBuilder'
import UploadMaterial from './screens/UploadMaterial'
import { type ApiReview, type ApiStudy, type ApiStudyStatus, createStudy, deleteStudy, getMe, listStudies, signOut } from './api'
import type { Identity } from './identity'
import { Banner, ScreenMessage, Spinner } from './components/ui'

// The report and review screens carry the Word editor (docx-editor -- most of the app's
// JavaScript), so they're only downloaded once one of them is opened.
const ReportGeneration = lazy(() => import('./screens/ReportGeneration'))
const Review = lazy(() => import('./screens/Review'))

export type Screen = 'dashboard' | 'setup' | 'builder' | 'upload' | 'report' | 'review'

// The workflow stage (see backend/app/db.py): building the study, then writing the report,
// then review -- each stage locks the one before it.
export type StudyStatus = ApiStudyStatus

export const isBuildStage = (status: StudyStatus) => status === 'draft' || status === 'in_progress'
export const isReviewStage = (status: StudyStatus) => status === 'in_review' || status === 'approved' || status === 'changes_requested'

// The frontend's own shape for a study -- a camelCase, UI-friendlier reshaping of
// ApiStudy (api.ts), converted by fromApi() below. Kept as a separate type (rather than
// just using ApiStudy directly) so screens can depend on stable field names/casing even
// if the wire format changes shape.
export interface Study {
  id: string
  name: string
  vessel: string
  loadcase: string
  systemType: string
  status: StudyStatus
  lastEdited: string
  project: string
  vesselLengthM: number | null
  vesselBreadthM: number | null
  vesselDepthM: number | null
  vesselDraftM: number | null
  ownerEmail: string
  ownerName: string
  collaborators: string[]
  archived: boolean
  revision: number
  review: ApiReview | null
}

// Whether `user` can edit `study` -- the owner, anyone explicitly granted access (see
// addCollaborator/removeCollaborator in api.ts), or an admin (see backend/app/roles.py's
// is_admin -- admins have owner-equivalent rights on every study). Read access is
// separate and universal (every study is listed/openable by everyone); this only gates the
// editing screens' mutating actions. `isAdmin` is purely a UI hint fetched once via
// getMe() -- mirrors backend/app/routers/studies.py's _require_edit, which is the actual
// authority; a frontend that got this wrong would just get a 403 back, never a security
// hole. Kept in sync by hand, same as every other frontend/backend pairing in this app.
export function canEditStudy(study: Study, user: Identity | null, isAdmin = false): boolean {
  if (!user) return false
  return isAdmin || study.ownerEmail === user.email || study.collaborators.includes(user.email)
}

export function isStudyOwner(study: Study, user: Identity | null): boolean {
  return Boolean(user) && study.ownerEmail === user!.email
}

export function awaitsReviewBy(study: Study, user: Identity | null): boolean {
  return Boolean(user) && study.status === 'in_review' && study.review?.reviewer_email === user!.email
}

// Where a study opens: the stage it's at (a study with no vessel yet is still in setup).
function stageScreen(study: Study): Screen {
  if (isReviewStage(study.status)) return 'review'
  if (study.status === 'reporting') return 'report'
  return study.vessel ? 'builder' : 'setup'
}

export function fromApi(s: ApiStudy): Study {
  return {
    id: s.id,
    name: s.name,
    vessel: s.vessel,
    loadcase: s.loadcase,
    systemType: s.system_type,
    status: s.status,
    lastEdited: new Date(s.updated_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
    project: s.project,
    vesselLengthM: s.vessel_length_m,
    vesselBreadthM: s.vessel_breadth_m,
    vesselDepthM: s.vessel_depth_m,
    vesselDraftM: s.vessel_draft_m,
    ownerEmail: s.owner_email,
    ownerName: s.owner_name,
    collaborators: s.collaborators,
    archived: s.archived,
    revision: s.revision,
    review: s.review ?? null,
  }
}

export default function App() {
  const [screen, setScreen] = useState<Screen>('dashboard')
  const [activeStudy, setActiveStudy] = useState<Study | null>(null)
  const [studies, setStudies] = useState<Study[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)
  // Who's signed in, from getMe() on load -- null until it answers (when signed out, it
  // never does: api.ts sends the browser to sign in instead).
  const [currentUser, setCurrentUser] = useState<Identity | null>(null)
  // From the same getMe() -- see canEditStudy's docstring for why this is a UI hint only,
  // not itself a permission check.
  const [isAdmin, setIsAdmin] = useState(false)
  // Authentik's sign-out page can take a few seconds to answer; until it does, the app is
  // replaced by a "Signing out…" notice rather than staying clickable.
  const [signingOut, setSigningOut] = useState(false)

  // Re-fetches the whole studies list (used on first mount and whenever navigation lands
  // back on the dashboard, e.g. after creating/deleting a study) -- `loadError` doubles
  // as both "network/backend down" state and the dashboard's error banner content.
  const refreshStudies = () => {
    listStudies()
      .then(({ studies }) => {
        setStudies(studies.map(fromApi))
        setLoadError(null)
      })
      .catch((err) => setLoadError(err.message || 'Could not reach the backend'))
  }

  useEffect(() => {
    getMe()
      .then((me) => {
        setCurrentUser({ email: me.email, name: me.name })
        setIsAdmin(me.is_admin)
        refreshStudies()
      })
      .catch((err) => setLoadError(err.message || 'Could not reach the backend'))
  }, [])

  // The one function every screen is handed as `onNav` -- switches which screen renders,
  // optionally updating which study is "active" at the same time (so a screen can e.g.
  // navigate to 'builder' *and* set which study that builder should show, in one call).
  // Always refreshes the studies list on the way back to the dashboard, so it reflects
  // whatever just changed (new study created, one deleted, a version generated, etc.).
  const navigate = (s: Screen, study?: Study) => {
    if (s === 'dashboard') refreshStudies()
    setScreen(s)
    if (study) setActiveStudy(study)
  }

  const openStudy = (study: Study) => navigate(stageScreen(study), study)
  const newStudy = () => {
    createStudy({})
      .then((s) => navigate('setup', fromApi(s)))
      .catch((err) => setLoadError(err.message || 'Could not create a new study'))
  }
  const removeStudy = (study: Study) => {
    deleteStudy(study.id)
      .then(() => refreshStudies())
      .catch((err) => setLoadError(err.message || 'Could not delete study'))
  }

  const startSignOut = () => {
    setSigningOut(true)
    signOut().catch((err) => {
      setSigningOut(false)
      setLoadError(err.message || 'Could not sign out')
    })
  }

  if (!currentUser || signingOut) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-bm-shade text-sm text-bm-subtle">
        {loadError && !signingOut ? (
          <Banner tone="error" title="Could not reach the backend">
            {loadError}
          </Banner>
        ) : (
          <>
            <Spinner />
            {signingOut ? 'Signing out…' : 'Signing in…'}
          </>
        )}
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col">
      {screen === 'dashboard' && (
        <StudiesDashboard
          studies={studies}
          currentUser={currentUser}
          isAdmin={isAdmin}
          onOpen={openStudy}
          onNew={newStudy}
          onDelete={removeStudy}
          onSignOut={startSignOut}
          loadError={loadError}
        />
      )}
      {screen === 'setup' && (
        <StudySetup study={activeStudy} onNav={navigate} />
      )}
      {screen === 'builder' && (
        <StudyBuilder study={activeStudy} onNav={navigate} currentUser={currentUser} isAdmin={isAdmin} />
      )}
      {screen === 'upload' && (
        <UploadMaterial study={activeStudy} onNav={navigate} currentUser={currentUser} isAdmin={isAdmin} />
      )}
      <Suspense fallback={<ScreenMessage />}>
        {screen === 'report' && (
          <ReportGeneration study={activeStudy} onNav={navigate} currentUser={currentUser} isAdmin={isAdmin} />
        )}
        {screen === 'review' && (
          <Review study={activeStudy} onNav={navigate} currentUser={currentUser} isAdmin={isAdmin} />
        )}
      </Suspense>
    </div>
  )
}
