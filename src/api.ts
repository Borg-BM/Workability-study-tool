// Thin fetch wrapper + one function/type per backend route (backend/app/routers/). There's
// no shared codegen with the backend --
// VersionParams/ScatterSource here have to be kept in sync BY HAND with backend/app/
// schemas.py's EnvironmentParams/ScatterSource; a field added on one side and not the
// other will silently fail (extra fields ignored by Pydantic, missing ones become null/
// undefined) rather than a type error, since JSON crosses the boundary untyped.

// Same origin by default: the API sits behind whatever serves the page (nginx in Docker,
// Vite's dev proxy locally), so the sign-in cookie is first-party. See vite.config.ts.
export const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ''

// Set while the page is on its way to signing in or out. A request answered 401 in the
// meantime must not start a navigation of its own: a sign-in started mid-sign-out cancels the
// sign-out, and Authentik -- still signed in -- sends you straight back.
let leaving = false

// Any 401 means "sign in (again)" -- the backend's session is gone or the Barge Master API
// stopped accepting it (see backend/app/sso.py). Authentik usually still has its own session,
// so this is a quick round trip back to the app rather than a password prompt.
function signIn(): void {
  if (leaving) return
  leaving = true
  window.location.assign(`${API_BASE}/api/auth/login?next=${encodeURIComponent(window.location.pathname)}`)
}

// Ends this app's session, then Authentik's -- otherwise the next visit signs straight back in.
export async function signOut(): Promise<void> {
  leaving = true
  try {
    const res = await fetch(`${API_BASE}/api/auth/logout`, { method: 'POST' })
    if (!res.ok) throw new ApiError(res.status, res.statusText || 'Could not sign out')
    const { logout_url } = await res.json()
    window.location.assign(logout_url)
  } catch (err) {
    leaving = false
    throw err
  }
}

// Carries the HTTP status alongside the message so callers can distinguish e.g. a 422
// (user-fixable CalculationError, safe to show as a form error) from a 404/500.
export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

// What to show for a failed call: the backend's own explanation (an ApiError's `detail`), or
// `fallback` for anything else (the network, a bug).
export const errorMessage = (err: unknown, fallback: string) => (err instanceof ApiError ? err.message : fallback)

// For reference lists that don't change while the app is open: fetched on first use, then
// shared by every screen that asks. A failed fetch isn't kept, so the next ask tries again.
function once<T>(load: () => Promise<T>): () => Promise<T> {
  let pending: Promise<T> | null = null
  return () => {
    if (!pending) {
      pending = load().catch((err) => {
        pending = null
        throw err
      })
    }
    return pending
  }
}

// Every exported function below is a thin call to this (via request()/requestBytes()): builds
// the full URL, defaults the body to JSON (unless it's a FormData, or the caller sets its own
// Content-Type), sends the browser off to sign in on a 401 (the session cookie is what tells
// the backend who's asking -- see backend/app/identity.py), and turns any other non-2xx
// response into a thrown ApiError with the backend's `detail` message when available
// (falling back to the raw status text if the error body isn't JSON).
async function send(path: string, init?: RequestInit): Promise<Response> {
  const isFormData = init?.body instanceof FormData
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
      ...(init?.headers || {}),
    },
  })
  if (res.status === 401) {
    signIn()
    // Never settles: the page is navigating away, so callers shouldn't flash an error first.
    return new Promise<Response>(() => {})
  }
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail || detail
    } catch {
      // Error response wasn't JSON (e.g. a raw 502 from something in front of the API) --
      // detail stays as res.statusText from above.
    }
    throw new ApiError(res.status, detail)
  }
  return res
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await send(path, init)
  // DELETE endpoints return 204 No Content -- .json() would throw on the empty body, so
  // short-circuit before attempting to parse one.
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

async function requestBytes(path: string, init?: RequestInit): Promise<Uint8Array<ArrayBuffer>> {
  const res = await send(path, init)
  return new Uint8Array(await res.arrayBuffer())
}

// ---- Identity ----

// Who's signed in (Authentik SSO, see backend/app/sso.py) -- the app's only source for the
// current user, and for is_admin, which the frontend has no way to know on its own (see
// backend/app/roles.py: the Authentik admin group). is_admin is a UI convenience only: every actual
// permission check still happens server-side on each real action, so this is just used to
// decide what to show (e.g. the Manage button on studies the caller doesn't own), never
// trusted in place of the backend's own 403s.
export interface ApiMe {
  email: string
  name: string
  is_admin: boolean
}
export const getMe = () => request<ApiMe>('/api/me')

// ---- Studies ----

// Where a study is in its workflow, which decides what can still be changed -- see
// backend/app/db.py's BUILD_STATUSES/REVIEW_STATUSES for the full meaning of each.
export type ApiStudyStatus = 'draft' | 'in_progress' | 'reporting' | 'in_review' | 'approved' | 'changes_requested'

// One report revision submitted for review, and the reviewer's decision on it.
export interface ApiReview {
  revision: number
  author_email: string
  author_name: string
  reviewer_email: string
  reviewer_name: string
  status: 'in_review' | 'approved' | 'changes_requested'
  comment: string
  submitted_at: string
  decided_at: string | null
}

export interface ApiStudy {
  id: string
  name: string
  vessel: string
  loadcase: string
  system_type: string
  project: string
  status: ApiStudyStatus
  // Report revision being worked on (Rev 0 first); bumped by startRevision.
  revision: number
  // The current revision's review, once it's been submitted (null before that).
  review?: ApiReview | null
  vessel_length_m: number | null
  vessel_breadth_m: number | null
  vessel_depth_m: number | null
  vessel_draft_m: number | null
  // The choices the report document is generated from (header fields, which study_files fill
  // which figure slot -- see reportModel.ts); the document itself is stored separately as a
  // .docx (getReportDocx). Opaque here for the reasons in backend/app/schemas.py's
  // SaveReportRequest docstring.
  report: Record<string, unknown>
  // The approved version the report document was generated from (null if unknown).
  report_version_id: string | null
  owner_email: string
  owner_name: string
  // Emails explicitly granted edit rights by the owner (see addCollaborator/
  // removeCollaborator) -- read access itself is universal, this only gates writes.
  collaborators: string[]
  // Display-state only (see archiveStudy/unarchiveStudy) -- hides the study from the
  // dashboard's main tabs without touching any of its actual data.
  archived: boolean
  created_at: string
  updated_at: string
}

// One piece of supporting material (photo, deck drawing, reference document) uploaded via
// UploadMaterial.tsx -- ReportGeneration.tsx picks specific ones by id to fill the
// report's figure slots (concept drawing, axis convention diagram, appendix images).
export interface ApiStudyFile {
  id: string
  study_id: string
  filename: string
  original_filename: string
  kind: 'image' | 'document'
  caption: string
  sort_order: number
  url: string
  created_at: string
}

// Mirrors run_calculation()'s return dict in backend/app/pybm_service.py (minus plot_png,
// which is written to disk server-side and exposed as ApiVersion.plot_url instead).
export interface WorkabilityRow {
  heading_from_deg: number
  heading_to_deg: number
  hs_limit_min_m: number
  hs_limit_max_m: number
  tp_min_s: number
  tp_max_s: number
}

export interface CalculationResult {
  overall_workability_pct: number | null
  // Seasonal breakdown by calendar month (e.g. { Jan: 95.6, ... }) -- every sample across
  // however many years the source data spans gets bucketed by its calendar month, so this
  // shows "how workable is a typical January" rather than a month-by-month project
  // timeline. Only available for a real dated time series (Copernicus/NDBC); null for a
  // statistical scatter source (DNV Weibull, uploaded scatter table), which has no dates
  // to bucket by -- see pybm_service.run_calculation's comment for the full reasoning.
  monthly_workability_pct: Record<string, number> | null
  worst_case: { heading_from_deg: number; heading_to_deg: number; hs_limit_min_m: number }
  table: WorkabilityRow[]
  location_label: string | null
  n_sigma_used: number | null
}

export interface ApiVersion {
  id: string
  study_id: string
  label: string
  diff_summary: string
  params: VersionParams
  result: CalculationResult
  plot_url: string | null
  approved: boolean
  created_at: string
}

// What GET /api/studies/{id} returns -- ApiStudy plus the study's full version history
// (list view GET /api/studies only returns bare ApiStudy rows, no versions, since the
// dashboard table doesn't need them).
export interface ApiStudyDetail extends ApiStudy {
  versions: ApiVersion[]
  files: ApiStudyFile[]
  // Whether a report document has been generated yet (see getReportDocx).
  has_report_docx: boolean
  review: ApiReview | null
  // Every submitted revision, oldest first.
  revisions: ApiRevision[]
}

// A submitted revision as the study detail lists it: its review, plus how many comment
// threads it got and how many of those are still open (see ReviewComments.tsx).
export interface ApiRevision extends ApiReview {
  comment_count: number
  open_comment_count: number
}

export const listStudies = () => request<{ studies: ApiStudy[] }>('/api/studies')
export const createStudy = (body: { name?: string; project?: string }) =>
  request<ApiStudy>('/api/studies', { method: 'POST', body: JSON.stringify(body) })
export const getStudy = (id: string) => request<ApiStudyDetail>(`/api/studies/${id}`)
export const deleteStudy = (id: string) => request<void>(`/api/studies/${id}`, { method: 'DELETE' })
export const updateStudy = (id: string, body: { name?: string; project?: string }) =>
  request<ApiStudy>(`/api/studies/${id}`, { method: 'PATCH', body: JSON.stringify(body) })

// "Copy to my studies" -- anyone can do this regardless of edit rights on the source (read
// access is universal); the backend creates a brand-new study owned by the caller, locked
// to the same vessel/loadcase/system_type, with a fresh version history.
export const copyStudy = (id: string) => request<ApiStudy>(`/api/studies/${id}/copy`, { method: 'POST' })

export const addCollaborator = (studyId: string, email: string) =>
  request<{ collaborators: string[] }>(`/api/studies/${studyId}/collaborators`, {
    method: 'POST',
    body: JSON.stringify({ email }),
  })

export const removeCollaborator = (studyId: string, email: string) =>
  request<{ collaborators: string[] }>(`/api/studies/${studyId}/collaborators/${encodeURIComponent(email)}`, {
    method: 'DELETE',
  })

export const archiveStudy = (id: string) => request<ApiStudy>(`/api/studies/${id}/archive`, { method: 'POST' })
export const unarchiveStudy = (id: string) => request<ApiStudy>(`/api/studies/${id}/unarchive`, { method: 'POST' })

// Reassigns the study to a new owner -- owner-or-admin only (see backend/app/
// routers/studies.py's transfer_ownership/_require_owner). For when the current owner
// leaves the company and someone needs to hand their studies off.
export const transferOwnership = (studyId: string, newOwnerEmail: string, newOwnerName?: string) =>
  request<ApiStudy>(`/api/studies/${studyId}/transfer`, {
    method: 'POST',
    body: JSON.stringify({ new_owner_email: newOwnerEmail, new_owner_name: newOwnerName }),
  })

export interface VesselDimensions {
  vessel_length_m: number | null
  vessel_breadth_m: number | null
  vessel_depth_m: number | null
  vessel_draft_m: number | null
}

export const setStudyRao = (
  studyId: string,
  vessel: string,
  loadcase: string,
  systemType: string,
  dims?: Partial<VesselDimensions>
) =>
  request<ApiStudy>(`/api/studies/${studyId}/rao`, {
    method: 'PUT',
    body: JSON.stringify({ vessel, loadcase, system_type: systemType, ...dims }),
  })

// Approving a result completes the build stage and locks the study builder (see reopenStudy).
export const approveVersion = (studyId: string, versionId: string) =>
  request<ApiVersion>(`/api/studies/${studyId}/versions/approve`, {
    method: 'POST',
    body: JSON.stringify({ version_id: versionId }),
  })

// Unlocks the study builder again -- only until the report is submitted for review.
export const reopenStudy = (studyId: string) => request<ApiStudyDetail>(`/api/studies/${studyId}/reopen`, { method: 'POST' })

export const uploadHindcast = (studyId: string, file: File) => {
  const form = new FormData()
  form.append('file', file)
  return request<{ id: string; filename: string }>(`/api/studies/${studyId}/hindcast-upload`, {
    method: 'POST',
    body: form,
  })
}

export const saveStudyReport = (studyId: string, report: Record<string, unknown>) =>
  request<{ report: Record<string, unknown> }>(`/api/studies/${studyId}/report`, {
    method: 'PUT',
    body: JSON.stringify({ report }),
  })

// ---- Report document (.docx) ----

export const DOCX_MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

// The study's report as Word document bytes (404s until one exists -- see has_report_docx).
export const getReportDocx = (studyId: string) => requestBytes(`/api/studies/${studyId}/report/docx`)

// The study plus its report document, if one has been generated yet.
export async function getStudyWithReport(studyId: string): Promise<[ApiStudyDetail, Uint8Array<ArrayBuffer> | null]> {
  const study = await getStudy(studyId)
  return [study, study.has_report_docx ? await getReportDocx(studyId) : null]
}

// (Re)builds the document from the saved header/figure choices (saveStudyReport) and the
// approved result -- replaces any existing document, edits included.
export const generateReportDocx = (studyId: string) =>
  request<void>(`/api/studies/${studyId}/report/docx/generate`, { method: 'POST' })

// Word comments are taken out on the way in (review comments live in the app), and the answer
// says how many there were.
export const saveReportDocx = (studyId: string, docx: Uint8Array<ArrayBuffer>) =>
  request<{ word_comments_removed: number }>(`/api/studies/${studyId}/report/docx`, { method: 'PUT', body: docx, headers: { 'Content-Type': DOCX_MIME } })

// Microsoft Word (or LibreOffice, without Word) on the backend does the conversion --
// docx-editor's own PDF export is a paid add-on.
export const convertDocxToPdf = (docx: Uint8Array<ArrayBuffer>) =>
  requestBytes('/api/convert/docx-to-pdf', { method: 'POST', body: docx, headers: { 'Content-Type': DOCX_MIME } })

// ---- Review ----

// The people allowed to review reports: the members of the Authentik reviewer group (see
// backend/app/roles.py). `restricted` is false when no group is configured -- then any
// colleague can be entered by email and name.
export interface ApiReviewer {
  email: string
  name: string
}
export const listReviewers = () => request<{ restricted: boolean; reviewers: ApiReviewer[] }>('/api/reviewers')

// Freezes the current revision and hands it to the reviewer, who becomes the document's Check.
export const submitForReview = (studyId: string, reviewerEmail: string, reviewerName: string) =>
  request<ApiStudyDetail>(`/api/studies/${studyId}/review`, {
    method: 'POST',
    body: JSON.stringify({ reviewer_email: reviewerEmail, reviewer_name: reviewerName }),
  })

export const changeReviewer = (studyId: string, reviewerEmail: string, reviewerName: string) =>
  request<ApiStudyDetail>(`/api/studies/${studyId}/review/reviewer`, {
    method: 'PUT',
    body: JSON.stringify({ reviewer_email: reviewerEmail, reviewer_name: reviewerName }),
  })

// Only the assigned reviewer can decide; requesting changes needs a comment.
export const decideReview = (studyId: string, decision: 'approve' | 'changes', comment: string) =>
  request<ApiStudyDetail>(`/api/studies/${studyId}/review/decision`, {
    method: 'POST',
    body: JSON.stringify({ decision, comment }),
  })

// Opens the next revision, starting from the last submitted document.
export const startRevision = (studyId: string) => request<ApiStudyDetail>(`/api/studies/${studyId}/revisions`, { method: 'POST' })

// A submitted revision's document, exactly as it was submitted.
export const getRevisionDocx = (studyId: string, revision: number) =>
  requestBytes(`/api/studies/${studyId}/revisions/${revision}/docx`)

// `docx` with revision `revision`'s comment threads in it as Word comments (replies threaded,
// resolved ones marked done) -- for rewriting the report in Word (backend/app/docx_comments.py).
export const docxWithComments = (studyId: string, revision: number, docx: Uint8Array<ArrayBuffer>) =>
  requestBytes(`/api/studies/${studyId}/revisions/${revision}/comments/docx`, { method: 'POST', body: docx, headers: { 'Content-Type': DOCX_MIME } })

// ---- Review comments ----

// One comment or reply on a submitted revision (backend/app/db.py's review_comments). A
// thread is a top-level comment plus the replies whose parent_id is its id; a thread made on
// a selection is anchored by para_id (the paragraph's w14:paraId) and quote (the selected text).
export interface ApiComment {
  id: string
  revision: number
  parent_id: string | null
  author_email: string
  author_name: string
  body: string
  para_id: string | null
  quote: string
  // Set on a resolved thread's top-level comment only.
  resolved_at: string | null
  resolved_by_name: string | null
  created_at: string
}

export const listComments = (studyId: string, revision: number) =>
  request<{ comments: ApiComment[] }>(`/api/studies/${studyId}/revisions/${revision}/comments`)
export const addComment = (studyId: string, revision: number, body: { body: string; parent_id?: string; para_id?: string; quote?: string }) =>
  request<ApiComment>(`/api/studies/${studyId}/revisions/${revision}/comments`, { method: 'POST', body: JSON.stringify(body) })
export const setCommentResolved = (studyId: string, commentId: string, resolved: boolean) =>
  request<ApiComment>(`/api/studies/${studyId}/comments/${commentId}`, { method: 'PATCH', body: JSON.stringify({ resolved }) })
export const deleteComment = (studyId: string, commentId: string) =>
  request<void>(`/api/studies/${studyId}/comments/${commentId}`, { method: 'DELETE' })

export const uploadStudyFile = (studyId: string, file: File, caption?: string) => {
  const form = new FormData()
  form.append('file', file)
  if (caption) form.append('caption', caption)
  return request<ApiStudyFile>(`/api/studies/${studyId}/files`, { method: 'POST', body: form })
}

export const updateStudyFile = (studyId: string, fileId: string, body: { caption?: string; sort_order?: number }) =>
  request<ApiStudyFile>(`/api/studies/${studyId}/files/${fileId}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  })

export const deleteStudyFile = (studyId: string, fileId: string) =>
  request<void>(`/api/studies/${studyId}/files/${fileId}`, { method: 'DELETE' })

// ---- RAOs ----

export const listVessels = once(() => request<{ vessels: string[] }>('/api/raos'))
export const listLoadcases = (vessel: string) =>
  request<{ loadcases: string[] }>(`/api/raos/${encodeURIComponent(vessel)}/loadcases`)
export const getRaoMetadata = (vessel: string, loadcase: string) =>
  request<{ vessel: string; loadcase: string; origin_m: number[] | null; attrs: Record<string, unknown> }>(
    `/api/raos/${encodeURIComponent(vessel)}/${encodeURIComponent(loadcase)}/metadata`
  )

// ---- Machines & locations ----

// `system_type` groups machine variants into the 3 top-level systems a study is fixed to
// once, at Study Setup -- StudyBuilder.tsx's "System" dropdown only offers the variants
// whose system_type matches the study's own (see ApiSystemType below).
export interface ApiMachine {
  id: string
  label: string
  system_type: string
  default_n_sigma: number | null
  needs_lifting_radius: boolean
  needs_comp_point_z: boolean
}

export const listMachines = once(() => request<{ machines: ApiMachine[] }>('/api/machines'))

export interface ApiSystemType {
  id: string
  label: string
}
export const listSystemTypes = once(() => request<{ system_types: ApiSystemType[] }>('/api/system-types'))

export interface ApiLocationBbox {
  lat_min: number
  lat_max: number
  lon_min: number
  lon_max: number
}
// One of the 104 DNV-RP-C205 nautic zones.
export interface ApiLocation {
  id: string
  label: string
  zone?: number
  bbox?: ApiLocationBbox
}
export const listLocations = once(() => request<{ locations: ApiLocation[] }>('/api/locations'))
export const listCopernicusProducts = once(() => request<{ products: { id: number; label: string }[] }>('/api/copernicus-products'))

// A real NOAA buoy with a confirmed historical wave record (see
// pybm_service.list_ndbc_buoys) -- `years` is the buoy's actual covered years, used by
// NdbcBuoyPickerModal.tsx's tooltip label and by StudyBuilder.tsx to steer the date range
// onto a period the picked buoy actually has data for. The backend's first answer after a
// restart takes a minute or two (it checks every buoy's record with NOAA), so StudyBuilder
// only asks once NDBC is picked as the source.
export interface ApiBuoy {
  id: string
  lat: number
  lon: number
  name: string | null
  years: number[]
}
export const listNdbcBuoys = once(() => request<{ buoys: ApiBuoy[] }>('/api/ndbc-buoys'))

// ---- Calculation ----

// Which of the four metocean data sources a study version uses (or none). Must match
// backend/app/schemas.py's ScatterSource Literal exactly -- see that file for what each
// value means and which of VersionParams.environment's fields apply to it.
export type ScatterSource = 'none' | 'weibull_builtin' | 'hindcast_upload' | 'copernicus' | 'ndbc'

// The full body of POST /api/studies/{id}/versions -- mirrors CreateVersionRequest in
// backend/app/schemas.py field-for-field (see that file's MachineParams/EnvironmentParams
// docstrings for what each field means; not re-documented here to avoid the two
// descriptions drifting out of sync with each other).
export interface VersionParams {
  machine: {
    machine_type: string
    position_x_m: number
    position_y_m: number
    position_z_m: number
    // MCG30 only
    luffing_angle_deg: number | null
    slewing_angle_deg: number | null
    dp_accuracy_m: number | null
    lifting_radius_m: number | null
    // T700 / Heavy Feeder family
    orientation_deg: number | null
    // T700 only
    p_passive_pa: number | null
    // Heavy Feeder family only
    comp_point_x_m: number | null
    comp_point_y_m: number | null
    comp_point_z_m: number | null
  }
  environment: {
    tp_min_s: number
    tp_max_s: number
    tp_step_s: number
    wave_dir_step_deg: number
    spreading: number
    standard_deviations: number | null
    scatter_source: ScatterSource
    location_id: string | null
    hindcast_upload_id: string | null
    hindcast_filename: string | null
    copernicus_lat: number | null
    copernicus_long: number | null
    copernicus_product_id: number
    copernicus_start_date: string | null
    copernicus_end_date: string | null
    ndbc_buoy_id: string | null
    ndbc_start_date: string | null
    ndbc_end_date: string | null
  }
}

export const createVersion = (studyId: string, params: VersionParams) =>
  request<ApiVersion>(`/api/studies/${studyId}/versions`, {
    method: 'POST',
    body: JSON.stringify(params),
  })
