import { useEffect, useMemo, useState } from 'react'
import { canEditStudy, fromApi, isBuildStage, type Study, type Screen } from '../App'
import type { Identity } from '../identity'
import Stepper from '../components/Stepper'
import LocationPickerModal from '../components/LocationPickerModal'
import WeibullZonePickerModal from '../components/WeibullZonePickerModal'
import NdbcBuoyPickerModal from '../components/NdbcBuoyPickerModal'
import PositionPickerModal from '../components/PositionPickerModal'
import ManageStudyModal from '../components/ManageStudyModal'
import { Banner, Button, EmptyState, Field, INPUT, LinkButton, PanelHeader, SectionTitle, Spinner, TABLE_HEAD_CELL, TopBar, UnitFieldGrid, UnitInput, buttonClass, choiceClass } from '../components/ui'
import {
  API_BASE,
  errorMessage,
  type ApiBuoy,
  type ApiLocation,
  type ApiMachine,
  type ApiVersion,
  type ScatterSource,
  type VersionParams,
  approveVersion,
  createVersion,
  deleteStudy,
  getRaoMetadata,
  getStudy,
  listCopernicusProducts,
  listLocations,
  listMachines,
  listNdbcBuoys,
  reopenStudy,
  uploadHindcast,
} from '../api'

// The main "2. Build study" workspace -- the biggest screen in the app. Three-part
// layout: a left column of machine/environment parameter inputs (including the 5-way
// metocean data source picker, each with its own sub-form and map-picker modal), a right
// column showing the active version's result (polar plot + summary + optional detail
// table), and a version tray letting the user flip between past calculation runs.
// buildParams() assembles everything the left column holds into one request; generate()
// sends it and shows a spinner while waiting for the real (potentially ~minute-long) response.
type ResultState = 'empty' | 'loading' | 'ready' | 'error'

export default function StudyBuilder({ study, onNav, currentUser, isAdmin }: { study: Study | null; onNav: (s: Screen, study?: Study) => void; currentUser: Identity; isAdmin: boolean }) {
  const [raoLoaded, setRaoLoaded] = useState(false)
  const [collaborators, setCollaborators] = useState<string[]>(study?.collaborators ?? [])
  const [archived, setArchived] = useState(study?.archived ?? false)
  // Local, patchable copies -- mirrors collaborators/archived above -- so a transfer (see
  // ManageStudyModal's onTransferred) updates this screen's own Manage-button visibility
  // and "View only" banner instantly, without waiting on a full study refetch.
  const [ownerEmail, setOwnerEmail] = useState(study?.ownerEmail ?? '')
  const [ownerName, setOwnerName] = useState(study?.ownerName ?? '')
  const [showManage, setShowManage] = useState(false)
  const isOwner = Boolean(study) && ownerEmail === currentUser.email
  const canManage = isOwner || isAdmin
  const canEdit = Boolean(study) && canEditStudy({ ...study!, collaborators, ownerEmail }, currentUser, isAdmin)

  // --- Machines & locations ---
  const [machines, setMachines] = useState<ApiMachine[]>([])
  const [locations, setLocations] = useState<ApiLocation[]>([])
  const [copernicusProducts, setCopernicusProducts] = useState<{ id: number; label: string }[]>([])
  const [ndbcBuoys, setNdbcBuoys] = useState<ApiBuoy[]>([])

  // --- Params ---
  const [machineType, setMachineType] = useState('')
  const [posX, setPosX] = useState('30.0')
  const [posY, setPosY] = useState('0.0')
  const [posZ, setPosZ] = useState('15.0')
  const [luffing, setLuffing] = useState('0')
  const [slewing, setSlewing] = useState('90')
  const [dpAccuracy, setDpAccuracy] = useState('0.5')
  const [liftingRadius, setLiftingRadius] = useState('18')
  const [orientation, setOrientation] = useState('0')
  const [pPassive, setPPassive] = useState('') // blank = PyBM's own T700 class default
  const [compPointX, setCompPointX] = useState('0')
  const [compPointY, setCompPointY] = useState('0')
  const [compPointZ, setCompPointZ] = useState('0')
  const [showPositionPicker, setShowPositionPicker] = useState(false)

  const [tpMin, setTpMin] = useState('4')
  const [tpMax, setTpMax] = useState('18')
  const [tpStep, setTpStep] = useState('2')
  const [waveDirStep, setWaveDirStep] = useState('30')
  const [spreading, setSpreading] = useState('3')
  const [nSigma, setNSigma] = useState('')
  const [scatterSource, setScatterSource] = useState<ScatterSource>('none')
  const [locationId, setLocationId] = useState('gws_zone_11')
  const [hindcastUpload, setHindcastUpload] = useState<{ id: string; filename: string } | null>(null)
  const [hindcastUploading, setHindcastUploading] = useState(false)
  const [hindcastError, setHindcastError] = useState<string | null>(null)
  const [copLat, setCopLat] = useState('')
  const [copLong, setCopLong] = useState('')
  const [copProductId, setCopProductId] = useState('0')
  // Blank start/end date means "use the whole available dataset" -- both PyBM loaders
  // treat None as "earliest/latest available" rather than requiring a specific range (see
  // pybm_service.py's copernicus/ndbc branches in _build_hindcast for how the actual
  // resolved range gets reported back once a calculation runs).
  const [copStart, setCopStart] = useState('')
  const [copEnd, setCopEnd] = useState('')
  const [ndbcBuoyId, setNdbcBuoyId] = useState('')
  const [ndbcStart, setNdbcStart] = useState('')
  const [ndbcEnd, setNdbcEnd] = useState('')
  const [showMapPicker, setShowMapPicker] = useState(false)
  const [showNdbcBuoyPicker, setShowNdbcBuoyPicker] = useState(false)
  const [showZonePicker, setShowZonePicker] = useState(false)

  // --- Result / versions ---
  const [resultState, setResultState] = useState<ResultState>('empty')
  const [calcError, setCalcError] = useState('')
  const [versions, setVersions] = useState<ApiVersion[]>([])
  const [activeVersionId, setActiveVersionId] = useState<string | null>(null)
  const [studyStatus, setStudyStatus] = useState(study?.status || 'draft')
  const [showDetailTable, setShowDetailTable] = useState(false)
  const [actionError, setActionError] = useState<string | null>(null)
  const [hasReport, setHasReport] = useState(false)
  // Approving a result completes this stage and locks the form; see reopen() for the way back.
  const buildOpen = isBuildStage(studyStatus)
  const editable = canEdit && buildOpen

  // Only machine variants belonging to this study's fixed system_type are ever
  // selectable -- e.g. a study fixed to "heavy_feeder" only offers HeavyFeeder and
  // HeavyFeederSurgeSway, never any MCG30/T700 variant (see StudySetup.tsx's system-type
  // picker + db.py's system_type column for where that's fixed).
  const filteredMachines = useMemo(
    () => machines.filter((m) => m.system_type === study?.systemType),
    [machines, study?.systemType]
  )
  const selectedMachine = machines.find((m) => m.id === machineType)
  const activeVersion = versions.find((v) => v.id === activeVersionId) || null
  const approvedVersion = versions.find((v) => v.approved) || null

  // The static picklists -- none of them depend on which study is open, and api.ts fetches
  // each only once per page load. Each fails silently (empty list on error) rather than
  // blocking the rest of the form on one broken endpoint.
  useEffect(() => {
    listMachines().then(({ machines }) => setMachines(machines)).catch(() => {})
    listLocations().then(({ locations }) => setLocations(locations)).catch(() => {})
    listCopernicusProducts().then(({ products }) => setCopernicusProducts(products)).catch(() => {})
  }, [])

  // The NDBC buoy list only once NDBC is the chosen source: the backend's first answer
  // checks every buoy's record with NOAA and takes a minute or two (see
  // pybm_service.list_ndbc_buoys). Until it arrives, the picker modal says it's loading.
  useEffect(() => {
    if (scatterSource !== 'ndbc' || ndbcBuoys.length > 0) return
    listNdbcBuoys().then(({ buoys }) => setNdbcBuoys(buoys)).catch(() => {})
  }, [scatterSource, ndbcBuoys.length])

  // Loads this study's version history whenever the study identity changes (re-runs if
  // the user navigates to a different study without a full page reload). If there's a
  // prior approved version, that's shown by default; otherwise the most recent one -- so
  // reopening a study lands back on whatever result was last worked on, not always the
  // first version.
  useEffect(() => {
    if (!study) return
    getStudy(study.id)
      .then((s) => {
        setVersions(s.versions)
        setStudyStatus(s.status)
        setHasReport(s.has_report_docx)
        if (s.versions.length > 0) {
          const approved = s.versions.find((v) => v.approved)
          const last = approved || s.versions[s.versions.length - 1]
          setActiveVersionId(last.id)
          setResultState('ready')
        }
      })
      .catch(() => {})
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [study?.id])

  // Confirms the RAO loads (the "RAO: vessel/loadcase" caption in the empty-result state
  // below) and, as a side effect, warms the backend's RAO cache so the first calculation
  // doesn't wait for it -- see routers/raos.py's get_metadata.
  useEffect(() => {
    if (!study?.vessel || !study.loadcase) return
    getRaoMetadata(study.vessel, study.loadcase)
      .then(() => setRaoLoaded(true))
      .catch(() => {})
  }, [study?.vessel, study?.loadcase])

  // Picks a default machineType once the machine list (and the study's system_type) are
  // known -- keeps the current selection if it's still a valid variant for this study
  // (e.g. flipping back from another study shouldn't reset an already-valid pick), and
  // otherwise falls back to the first variant of this study's system type.
  useEffect(() => {
    if (filteredMachines.length === 0) return
    if (filteredMachines.some((m) => m.id === machineType)) return
    setMachineType(filteredMachines[0].id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filteredMachines])

  // Each machine type has its own sensible default n-sigma (see MACHINE_TYPES in
  // pybm_service.py) -- re-apply it whenever the system changes, so switching from a
  // transfer to a lifting machine doesn't silently keep the wrong default. This only ever
  // *sets* nSigma, never clears it back to blank, so a value the user typed by hand
  // survives until they pick a different machine.
  useEffect(() => {
    if (selectedMachine?.default_n_sigma != null) setNSigma(String(selectedMachine.default_n_sigma))
  }, [machineType, selectedMachine])

  const onHindcastFile = (file: File) => {
    if (!study) return
    setHindcastUploading(true)
    setHindcastError(null)
    uploadHindcast(study.id, file)
      .then((res) => setHindcastUpload(res))
      .catch((err) => setHindcastError(errorMessage(err, 'Upload failed')))
      .finally(() => setHindcastUploading(false))
  }

  // Assembles the full request body for POST .../versions. VersionParams' shape requires
  // every scatter-source-specific field to be present regardless of which source is
  // active (see api.ts/schemas.py) -- so every branch below sets its own fields from the
  // matching state and explicitly nulls out the ones for sources that aren't selected,
  // rather than only including the "relevant" subset. This keeps the backend's
  // scatter_source-gated logic (pybm_service._build_hindcast) as the single source of
  // truth for which fields actually matter, instead of duplicating that logic here.
  const buildParams = (): VersionParams | null => {
    if (!study?.vessel) return null
    const environment: VersionParams['environment'] = {
      tp_min_s: parseFloat(tpMin),
      tp_max_s: parseFloat(tpMax),
      tp_step_s: parseFloat(tpStep),
      wave_dir_step_deg: parseFloat(waveDirStep),
      spreading: parseFloat(spreading),
      standard_deviations: nSigma.trim() === '' ? null : parseFloat(nSigma),
      scatter_source: scatterSource,
      location_id: scatterSource === 'weibull_builtin' ? locationId : null,
      hindcast_upload_id: scatterSource === 'hindcast_upload' ? hindcastUpload?.id || null : null,
      hindcast_filename: scatterSource === 'hindcast_upload' ? hindcastUpload?.filename || null : null,
      copernicus_lat: scatterSource === 'copernicus' ? parseFloat(copLat) : null,
      copernicus_long: scatterSource === 'copernicus' ? parseFloat(copLong) : null,
      copernicus_product_id: parseInt(copProductId, 10), // sent regardless of scatterSource, unlike lat/long/dates -- harmless, since the backend only reads it when scatter_source == "copernicus" and it defaults to 0
      copernicus_start_date: scatterSource === 'copernicus' ? copStart || null : null,
      copernicus_end_date: scatterSource === 'copernicus' ? copEnd || null : null,
      ndbc_buoy_id: scatterSource === 'ndbc' && ndbcBuoyId.trim() !== '' ? ndbcBuoyId.trim() : null,
      ndbc_start_date: scatterSource === 'ndbc' ? ndbcStart || null : null,
      ndbc_end_date: scatterSource === 'ndbc' ? ndbcEnd || null : null,
    }
    const systemType = selectedMachine?.system_type
    return {
      machine: {
        machine_type: machineType,
        position_x_m: parseFloat(posX),
        position_y_m: parseFloat(posY),
        position_z_m: parseFloat(posZ),
        luffing_angle_deg: systemType === 'mcg30' ? parseFloat(luffing) : null,
        slewing_angle_deg: systemType === 'mcg30' ? parseFloat(slewing) : null,
        dp_accuracy_m: systemType === 'mcg30' ? parseFloat(dpAccuracy) : null,
        lifting_radius_m: selectedMachine?.needs_lifting_radius ? parseFloat(liftingRadius) : null,
        orientation_deg: systemType === 't700' || systemType === 'heavy_feeder' ? parseFloat(orientation) : null,
        p_passive_pa: systemType === 't700' && pPassive.trim() !== '' ? parseFloat(pPassive) : null,
        comp_point_x_m: systemType === 'heavy_feeder' ? parseFloat(compPointX) : null,
        comp_point_y_m: systemType === 'heavy_feeder' ? parseFloat(compPointY) : null,
        comp_point_z_m: systemType === 'heavy_feeder' ? parseFloat(compPointZ) : null,
      },
      environment,
    }
  }

  // "Generate" is disabled until the currently-selected scatter source has whatever it
  // specifically needs (an uploaded file, a picked lat/long, a picked buoy) -- sources
  // that need nothing extra (none/weibull_builtin) just fall through their
  // `scatterSource !== '...'` check as true.
  const canGenerate =
    editable &&
    Boolean(study?.vessel) &&
    (scatterSource !== 'hindcast_upload' || Boolean(hindcastUpload)) &&
    (scatterSource !== 'copernicus' || (copLat.trim() !== '' && copLong.trim() !== '')) &&
    (scatterSource !== 'ndbc' || ndbcBuoyId.trim() !== '') &&
    resultState !== 'loading'

  // Kicks off a real calculation (createVersion -- can genuinely take up to ~a minute,
  // longer for Copernicus/NDBC downloads). It's one blocking request with no progress signal,
  // so the loading state is just a spinner, not a progress bar.
  const generate = () => {
    if (!study) return
    const params = buildParams()
    if (!params) return

    setResultState('loading')
    createVersion(study.id, params)
      .then((version) => {
        setVersions((vs) => [...vs, version])
        setActiveVersionId(version.id)
        setResultState('ready')
        setShowDetailTable(false)
        setStudyStatus('in_progress')
      })
      .catch((err) => {
        setCalcError(errorMessage(err, 'The calculation engine returned an error.'))
        setResultState('error')
      })
  }

  // Approving the currently-viewed version completes this stage: the study locks and moves on
  // to Upload material (only one version is ever approved, see db.approve_version).
  const approve = async () => {
    if (!study || !activeVersion) return
    if (!window.confirm(`Approve ${activeVersion.label} and lock the study? The study builder becomes view-only; you can reopen it until the report is submitted for review.`)) return
    setActionError(null)
    try {
      await approveVersion(study.id, activeVersion.id)
      onNav('upload', fromApi(await getStudy(study.id)))
    } catch (err) {
      setActionError(errorMessage(err, 'Could not approve this result'))
    }
  }

  // The deliberate way back into a completed study, while its report isn't in review yet.
  const reopen = async () => {
    if (!study) return
    if (!window.confirm('Reopen the study? You can generate new results and approve a different one. If the approved result changes, regenerate the report afterwards so it uses the new one.')) return
    setActionError(null)
    try {
      const updated = await reopenStudy(study.id)
      setStudyStatus(updated.status)
      onNav('builder', fromApi(updated))
    } catch (err) {
      setActionError(errorMessage(err, 'Could not reopen the study'))
    }
  }

  // A study can exist without a vessel/loadcase yet (created but StudySetup wasn't
  // finished) -- bail out to a "go finish setup" prompt rather than rendering a form for
  // parameters that need a RAO to mean anything.
  if (!study?.vessel) {
    return (
      <div className="flex min-h-screen bg-bm-shade">
        <Stepper screen="builder" status={studyStatus} reportGenerated={hasReport} onNav={onNav} />
        <div className="flex-1 flex flex-col min-w-0">
          <TopBar onBack={() => onNav('dashboard')} title={study?.name || 'New study'} status={studyStatus} />
          <EmptyState title="No RAO set for this study yet" action={<Button onClick={() => onNav('setup', study || undefined)}>Go to setup</Button>}>
            Finish the study setup step first.
          </EmptyState>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen bg-bm-shade">
      <Stepper screen="builder" status={studyStatus} reportGenerated={hasReport} onNav={onNav} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar
          onBack={() => onNav('dashboard')}
          title={study?.name || 'New study'}
          status={studyStatus}
          meta={`${study.vessel} · ${study.loadcase}${study.project ? ` · ${study.project}` : ''}`}
        >
          {!canEdit && <span className="text-xs font-bold px-2 py-0.5 rounded bg-bm-warning-tint text-bm-warning">View only</span>}
          {canManage && (
            <Button variant="secondary" size="sm" onClick={() => setShowManage(true)}>
              Manage{collaborators.length > 0 ? ` (${collaborators.length} shared)` : ''}
            </Button>
          )}
        </TopBar>

        {!buildOpen && (
          <Banner
            tone="info"
            bar
            action={
              studyStatus === 'reporting' && canEdit ? (
                <Button variant="secondary" size="sm" onClick={reopen}>
                  Reopen study
                </Button>
              ) : undefined
            }
          >
            <strong>🔒 Study complete.</strong>{' '}
            {studyStatus === 'reporting'
              ? `The approved result${approvedVersion ? ` (${approvedVersion.label})` : ''} is locked and used for the report.`
              : `Revision ${study.revision} of the report has been submitted for review, so the study is locked. Changes need a new revision, started from the Review page.`}
          </Banner>
        )}
        {actionError && (
          <Banner tone="error" bar>
            {actionError}
          </Banner>
        )}

        <div className="flex flex-1 min-h-0">
          {/* Col 1: Parameters */}
          <div className="w-80 flex-shrink-0 flex flex-col border-r border-bm-rule bg-white">
            <PanelHeader title="System & environment" />

            {/* A disabled fieldset locks every input, select and picker button inside it at once. */}
            <fieldset disabled={!editable} className="flex-1 px-4 py-4 flex flex-col gap-6 min-w-0">
              <section>
                <div className="flex flex-col gap-3">
                  <Field label="System">
                    <select className={INPUT} value={machineType} onChange={(e) => setMachineType(e.target.value)}>
                      {filteredMachines.map((m) => (
                        <option key={m.id} value={m.id}>
                          {m.label}
                        </option>
                      ))}
                    </select>
                  </Field>
                  {selectedMachine?.system_type === 'mcg30' && (
                    <>
                      <Field label="Luffing angle">
                        <UnitInput unit="deg" type="number" value={luffing} onChange={(e) => setLuffing(e.target.value)} />
                      </Field>
                      <Field label="DP accuracy">
                        <UnitInput unit="m" type="number" value={dpAccuracy} onChange={(e) => setDpAccuracy(e.target.value)} />
                      </Field>
                      {selectedMachine?.needs_lifting_radius && (
                        <Field label="Lifting radius">
                          <UnitInput unit="m" type="number" value={liftingRadius} onChange={(e) => setLiftingRadius(e.target.value)} />
                        </Field>
                      )}
                    </>
                  )}
                  {(selectedMachine?.system_type === 't700' || selectedMachine?.system_type === 'heavy_feeder') && (
                    <>
                      {selectedMachine?.system_type === 't700' && (
                        <Field label="Passive pressure (P_passive)">
                          <UnitInput unit="Pa" type="number" value={pPassive} onChange={(e) => setPPassive(e.target.value)} placeholder="engine default" />
                        </Field>
                      )}
                      {selectedMachine?.system_type === 'heavy_feeder' && (
                        <div>
                          <div className="text-xs font-bold mb-1 text-bm-text">Compensation point (w.r.t. central bearing)</div>
                          {selectedMachine?.needs_comp_point_z && (
                            <p className="text-xs mb-1.5 text-bm-warning">Z must be above the central bearing (&gt; 0) to compensate surge/sway motion.</p>
                          )}
                          <UnitFieldGrid
                            unit="m"
                            className="grid-cols-3 gap-1.5"
                            fields={[
                              ['X', compPointX, setCompPointX],
                              ['Y', compPointY, setCompPointY],
                              ['Z', compPointZ, setCompPointZ],
                            ]}
                          />
                        </div>
                      )}
                    </>
                  )}
                </div>
              </section>

              <section>
                <SectionTitle>Position & heading (w.r.t. APP/CL/K)</SectionTitle>
                <div className="flex flex-col gap-3">
                  <UnitFieldGrid
                    unit="m"
                    className="grid-cols-3 gap-1.5"
                    fields={[
                      ['X', posX, setPosX],
                      ['Y', posY, setPosY],
                      ['Z', posZ, setPosZ],
                    ]}
                  />
                  {/* The heading sits with the position: the ship picker below sets both. */}
                  {selectedMachine?.system_type === 'mcg30' && (
                    <Field label="Slewing angle" hint="90° = port side, 270° = starboard side">
                      <UnitInput unit="deg" type="number" value={slewing} onChange={(e) => setSlewing(e.target.value)} />
                    </Field>
                  )}
                  {(selectedMachine?.system_type === 't700' || selectedMachine?.system_type === 'heavy_feeder') && (
                    <Field label="Orientation" hint={selectedMachine?.system_type === 'heavy_feeder' ? '0° = cylinders on port side' : undefined}>
                      <UnitInput unit="deg" type="number" value={orientation} onChange={(e) => setOrientation(e.target.value)} />
                    </Field>
                  )}
                  <Button variant="outline" className="w-full" onClick={() => setShowPositionPicker(true)}>
                    Pick position & heading on ship ↗
                  </Button>
                </div>
              </section>

              <section>
                <SectionTitle>Sea state (Tp) & wave</SectionTitle>
                <div className="flex flex-col gap-3">
                  <UnitFieldGrid
                    unit="s"
                    className="grid-cols-3 gap-1.5"
                    fields={[
                      ['Tp min', tpMin, setTpMin],
                      ['Tp max', tpMax, setTpMax],
                      ['Tp step', tpStep, setTpStep],
                    ]}
                  />
                  <Field label="Wave heading step">
                    <UnitInput unit="deg" type="number" value={waveDirStep} onChange={(e) => setWaveDirStep(e.target.value)} />
                  </Field>
                  <Field label="Wave spreading">
                    <input className={INPUT} type="number" value={spreading} onChange={(e) => setSpreading(e.target.value)} />
                  </Field>
                  <Field label="Std. deviations (n-sigma)">
                    <input
                      className={INPUT}
                      type="number"
                      placeholder={selectedMachine?.default_n_sigma != null ? `default: ${selectedMachine.default_n_sigma}` : 'engine default (MPE)'}
                      value={nSigma}
                      onChange={(e) => setNSigma(e.target.value)}
                    />
                  </Field>
                </div>
              </section>

              <section>
                <SectionTitle hint="Without this, you'll get the operating envelope — which sea states the system can handle. With it, you also get an overall workability %.">
                  Metocean data (optional)
                </SectionTitle>
                <div className="flex flex-col gap-3">
                  {/* Ordered by PyBM's own documented priority for choosing a hindcast
                      source (docs/usage/hindcast.md, "How to choose the right loader?"):
                      client-provided data first, then a real measured/reanalysis source by
                      coordinate, and DNV Weibull statistics only as a last resort. */}
                  <select className={INPUT} value={scatterSource} onChange={(e) => setScatterSource(e.target.value as ScatterSource)}>
                    <option value="none">None — envelope only</option>
                    <option value="hindcast_upload">Hindcast scatter table (upload .xlsx) — preferred, client data</option>
                    <option value="copernicus">Copernicus Marine (real wave data)</option>
                    <option value="ndbc">NOAA NDBC buoy (real measured data, US coastal)</option>
                    <option value="weibull_builtin">DNV Weibull (built-in location) — last resort</option>
                  </select>

                  {scatterSource === 'weibull_builtin' && (
                    <>
                      <p className="text-xs text-bm-warning">
                        Last resort — DNV C205 Weibull results are highly conservative; if used in client communication, pair with a base-case comparison.
                      </p>
                      <select className={INPUT} value={locationId} onChange={(e) => setLocationId(e.target.value)}>
                        {locations.map((l) => (
                          <option key={l.id} value={l.id}>
                            {l.label}
                          </option>
                        ))}
                      </select>
                      <Button variant="outline" size="sm" className="self-start" onClick={() => setShowZonePicker(true)}>
                        🗺 Pick zone on map
                      </Button>
                    </>
                  )}

                  {scatterSource === 'hindcast_upload' && (
                    <>
                      <div className="flex gap-1.5">
                        {/* The native <input type="file"> can't be restyled directly (its button
                            chrome is OS-drawn), so it's hidden and triggered by a <label>. */}
                        <label className={buttonClass('outline', 'sm', 'cursor-pointer')}>
                          📄 Upload scatter table
                          <input type="file" accept=".xlsx" onChange={(e) => e.target.files?.[0] && onHindcastFile(e.target.files[0])} className="hidden" />
                        </label>
                        <a href="/HindcastScatterTable_template.xlsx" download className={buttonClass('neutral', 'sm')}>
                          ⬇ Template
                        </a>
                      </div>
                      {hindcastUploading && <p className="text-xs text-bm-subtle">Uploading…</p>}
                      {hindcastUpload && <p className="text-xs font-bold text-bm-success">✓ {hindcastUpload.filename}</p>}
                      {hindcastError && <p className="text-xs text-bm-danger-text">{hindcastError}</p>}
                      <p className="text-xs text-bm-subtle">Format: sheet named "Hs-Tp" or "Tp-Hs" -- see the template.</p>
                    </>
                  )}

                  {scatterSource === 'copernicus' && (
                    <>
                      <div className="grid grid-cols-2 gap-1.5">
                        <Field label="Latitude">
                          <input className={INPUT} type="number" value={copLat} onChange={(e) => setCopLat(e.target.value)} placeholder="54.0" />
                        </Field>
                        <Field label="Longitude">
                          <input className={INPUT} type="number" value={copLong} onChange={(e) => setCopLong(e.target.value)} placeholder="3.0" />
                        </Field>
                      </div>
                      <Button variant="outline" size="sm" className="self-start" onClick={() => setShowMapPicker(true)}>
                        🗺 Pick on map
                      </Button>
                      <Field label="Product / region">
                        <select className={INPUT} value={copProductId} onChange={(e) => setCopProductId(e.target.value)}>
                          {copernicusProducts.map((p) => (
                            <option key={p.id} value={p.id}>
                              {p.label}
                            </option>
                          ))}
                        </select>
                      </Field>
                      <div className="grid grid-cols-2 gap-1.5">
                        <Field label="Start date (optional)">
                          <input className={INPUT} type="date" value={copStart} onChange={(e) => setCopStart(e.target.value)} />
                        </Field>
                        <Field label="End date (optional)">
                          <input className={INPUT} type="date" value={copEnd} onChange={(e) => setCopEnd(e.target.value)} />
                        </Field>
                      </div>
                      <p className="text-xs text-bm-subtle">
                        Fetches real reanalysis wave data — leave the dates blank to use the whole available dataset, or narrow the range if you only want a specific period.
                        Preferred over NDBC for anywhere outside North American coastal waters.
                      </p>
                    </>
                  )}

                  {scatterSource === 'ndbc' && (
                    <>
                      <Field label="Buoy ID">
                        <input className={INPUT} value={ndbcBuoyId} onChange={(e) => setNdbcBuoyId(e.target.value)} placeholder="e.g. 44008 — pick one on the map" />
                      </Field>
                      <div className="flex gap-1.5">
                        <Button variant="outline" size="sm" onClick={() => setShowNdbcBuoyPicker(true)}>
                          🗺 Pick on map
                        </Button>
                        <a href="https://www.ndbc.noaa.gov/" target="_blank" rel="noopener noreferrer" className={buttonClass('neutral', 'sm')}>
                          ndbc.noaa.gov ↗
                        </a>
                      </div>
                      <div className="grid grid-cols-2 gap-1.5">
                        <Field label="Start date (optional)">
                          <input className={INPUT} type="date" value={ndbcStart} onChange={(e) => setNdbcStart(e.target.value)} />
                        </Field>
                        <Field label="End date (optional)">
                          <input className={INPUT} type="date" value={ndbcEnd} onChange={(e) => setNdbcEnd(e.target.value)} />
                        </Field>
                      </div>
                      <p className="text-xs text-bm-subtle">
                        Real measured buoy data — pick an actual buoy rather than typing coordinates, so you know the reading is from your site and not from whatever buoy happens to be nearest (which can be hundreds of km away). Only buoys with a real historical record are offered. Leave the dates blank to use the buoy's whole available record; if you've set a specific range, picking a buoy snaps it onto a period that buoy actually covers. Suitable for North American / US coastal waters — use Copernicus Marine for anywhere else.
                      </p>
                    </>
                  )}
                </div>
              </section>
            </fieldset>

            {buildOpen && (
              <div className="px-4 py-3 border-t border-bm-rule bg-bm-shade sticky bottom-0">
                <Button className="w-full" onClick={generate} disabled={!canGenerate}>
                  {resultState === 'loading' ? 'Calculating…' : 'Generate workability study'}
                </Button>
              </div>
            )}
          </div>

          {/* Col 2: Result */}
          <div className="flex-1 flex flex-col min-w-0">
            {/* Version tray -- the same height as the parameters' title bar beside it */}
            {versions.length > 0 && (
              <div className="flex-shrink-0 flex items-center gap-1.5 px-6 min-h-11 border-b border-bm-rule bg-bm-shade overflow-x-auto">
                <span className="text-xs font-bold uppercase tracking-widest mr-2 text-bm-navy">Versions</span>
                {versions.map((v) => (
                  <button
                    key={v.id}
                    onClick={() => {
                      setActiveVersionId(v.id)
                      setResultState('ready')
                    }}
                    className={choiceClass(activeVersionId === v.id, 'sm')}
                  >
                    {v.label}
                    {v.approved && <span>✓</span>}
                    <span className="font-normal opacity-70">{v.diff_summary}</span>
                  </button>
                ))}
              </div>
            )}

            <div className="flex-1 overflow-y-auto">
              {resultState === 'empty' && (
                <EmptyState icon="◎" title="Result">
                  Configure the system parameters, then click "Generate workability study". A polar workability plot will appear here.
                  {raoLoaded && (
                    <p className="text-xs mt-4 text-bm-placeholder">
                      RAO: {study.vessel} / {study.loadcase}
                    </p>
                  )}
                </EmptyState>
              )}

              {resultState === 'loading' && (
                <EmptyState icon={<Spinner />} title="Running calculation engine…">
                  Calculations may take up to a minute.
                </EmptyState>
              )}

              {resultState === 'error' && (
                <EmptyState icon="⚠" title="Calculation failed" action={<Button onClick={generate}>Retry calculation</Button>}>
                  {calcError}
                </EmptyState>
              )}

              {resultState === 'ready' && activeVersion && (
                <div className="px-6 py-5 flex flex-col gap-6">
                  <section>
                    <SectionTitle>Result — {activeVersion.label}</SectionTitle>
                    <div className="flex gap-6 flex-wrap items-start">
                      {/* Polar plot — the primary output */}
                      {activeVersion.plot_url && (
                        <img src={`${API_BASE}${activeVersion.plot_url}`} alt="Workability polar plot" className="flex-shrink-0 bg-white border border-bm-rule rounded" style={{ width: 380 }} />
                      )}
                      <div className="flex-1 flex flex-col gap-4" style={{ minWidth: 200 }}>
                        {activeVersion.result.overall_workability_pct != null ? (
                          <div className="rounded border p-4 bg-bm-tint border-bm-blue">
                            <div className="text-xs font-bold uppercase tracking-wide mb-1 text-bm-blue-dark">Overall workability</div>
                            <div className="text-4xl font-bold text-bm-navy">{activeVersion.result.overall_workability_pct}%</div>
                            <div className="text-xs mt-1 text-bm-muted">{activeVersion.result.location_label}</div>
                          </div>
                        ) : (
                          <Banner tone="neutral">No metocean data provided — showing the operating envelope only, no overall %.</Banner>
                        )}
                        <div className="rounded border p-4 bg-bm-warning-tint border-bm-warning-rule">
                          <div className="text-xs font-bold uppercase tracking-wide mb-1 text-bm-warning">Worst case</div>
                          <div className="text-sm font-bold text-bm-ink">
                            Heading {String(activeVersion.result.worst_case.heading_from_deg).padStart(3, '0')}° — {String(activeVersion.result.worst_case.heading_to_deg).padStart(3, '0')}°
                          </div>
                          <div className="text-xs mt-0.5 text-bm-muted">Limiting Hs {activeVersion.result.worst_case.hs_limit_min_m} m</div>
                        </div>
                      </div>
                    </div>
                  </section>

                  {activeVersion.result.monthly_workability_pct && (
                    <section>
                      <SectionTitle hint="Seasonal average per calendar month across the full dataset — useful for a project that only runs part of the year.">Monthly breakdown</SectionTitle>
                      <div className="flex flex-wrap gap-1.5">
                        {Object.entries(activeVersion.result.monthly_workability_pct).map(([month, pct]) => (
                          <div
                            key={month}
                            className={`rounded border px-2.5 py-1.5 text-center ${pct >= 70 ? 'border-bm-success-rule bg-bm-success-tint' : 'border-bm-warning-rule bg-bm-warning-tint'}`}
                            style={{ minWidth: 56 }}
                          >
                            <div className="text-xs font-bold uppercase text-bm-subtle">{month}</div>
                            <div className={`text-sm font-bold ${pct >= 70 ? 'text-bm-success' : 'text-bm-warning'}`}>{pct}%</div>
                          </div>
                        ))}
                      </div>
                    </section>
                  )}

                  <section>
                    <SectionTitle
                      aside={
                        <LinkButton onClick={() => setShowDetailTable((v) => !v)}>{showDetailTable ? '▾ Hide' : '▸ Show'}</LinkButton>
                      }
                    >
                      Per-heading detail
                    </SectionTitle>
                    {showDetailTable && (
                      <div className="bg-white border border-bm-rule rounded overflow-hidden">
                        <table className="w-full text-xs border-collapse">
                          <thead>
                            <tr>
                              {['Heading', 'Hs limit (m)', 'Tp range (s)'].map((h) => (
                                <th key={h} className={TABLE_HEAD_CELL}>
                                  {h}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {activeVersion.result.table.map((row) => {
                              const isWorst = row.heading_from_deg === activeVersion.result.worst_case.heading_from_deg
                              return (
                                <tr key={row.heading_from_deg} className={`border-b border-bm-rule-light last:border-b-0 ${isWorst ? 'bg-bm-warning-tint' : ''}`}>
                                  <td className="px-4 py-2 font-bold text-bm-navy">
                                    {String(row.heading_from_deg).padStart(3, '0')}° – {String(row.heading_to_deg).padStart(3, '0')}°
                                  </td>
                                  <td className="px-4 py-2">
                                    {row.hs_limit_min_m} – {row.hs_limit_max_m}
                                  </td>
                                  <td className="px-4 py-2">
                                    {row.tp_min_s} – {row.tp_max_s}
                                  </td>
                                </tr>
                              )
                            })}
                          </tbody>
                        </table>
                      </div>
                    )}
                    {activeVersion.result.n_sigma_used != null && (
                      <p className="text-xs mt-2 text-bm-subtle">Standard deviations (n-sigma) used: {activeVersion.result.n_sigma_used}</p>
                    )}
                  </section>
                </div>
              )}
            </div>

            {/* Decision bar */}
            {resultState === 'ready' && activeVersion && (buildOpen || approvedVersion?.id === activeVersion.id) && (
              <div className="flex-shrink-0 px-6 py-3 border-t border-bm-rule bg-bm-shade flex items-center justify-between sticky bottom-0">
                <div className="text-xs font-bold uppercase tracking-widest text-bm-navy">Decision</div>
                {buildOpen ? (
                  <div className="flex gap-2">
                    <Button variant="neutral" onClick={() => setResultState('empty')} disabled={!editable}>
                      Adjust parameters
                    </Button>
                    <Button variant="dark" onClick={approve} disabled={!editable}>
                      Approve &amp; lock this result →
                    </Button>
                  </div>
                ) : (
                  <span className="px-3 py-1.5 text-sm font-bold rounded bg-bm-tint text-bm-blue-dark">✓ Approved result</span>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      {/* The three map-picker modals: each is only mounted while its `show*` flag is
          true (rather than always-mounted-but-hidden), so each one's Leaflet map is torn
          down and recreated fresh every time it's opened -- simpler than keeping a
          persistent map instance in sync with a hidden/visible toggle. */}
      {showMapPicker && (
        <LocationPickerModal
          initialLat={copLat ? parseFloat(copLat) : null}
          initialLng={copLong ? parseFloat(copLong) : null}
          onClose={() => setShowMapPicker(false)}
          onConfirm={(lat, lng) => {
            setCopLat(lat.toFixed(4))
            setCopLong(lng.toFixed(4))
            setShowMapPicker(false)
          }}
        />
      )}
      {showNdbcBuoyPicker && (
        <NdbcBuoyPickerModal
          buoys={ndbcBuoys}
          initialBuoyId={ndbcBuoyId || null}
          onClose={() => setShowNdbcBuoyPicker(false)}
          onConfirm={(buoyId) => {
            setNdbcBuoyId(buoyId)
            // Blank dates mean "use the buoy's whole record" -- trivially "covered" by any
            // buoy with any history at all, so leave them alone. Only steer an *explicit*
            // range the user already set onto a period this buoy actually has data for,
            // rather than silently keeping a range that isn't covered.
            const buoy = ndbcBuoys.find((b) => b.id === buoyId)
            if (buoy && buoy.years.length > 0 && ndbcStart.trim() !== '' && ndbcEnd.trim() !== '') {
              const startYear = parseInt(ndbcStart.slice(0, 4), 10)
              const endYear = parseInt(ndbcEnd.slice(0, 4), 10)
              const covered = buoy.years.includes(startYear) && buoy.years.includes(endYear)
              if (!covered) {
                const latestYear = Math.max(...buoy.years)
                setNdbcStart(`${latestYear}-01-01`)
                setNdbcEnd(`${latestYear}-12-31`)
              }
            }
            setShowNdbcBuoyPicker(false)
          }}
        />
      )}
      {showZonePicker && (
        <WeibullZonePickerModal
          locations={locations}
          initialLocationId={locationId}
          onClose={() => setShowZonePicker(false)}
          onConfirm={(id) => {
            setLocationId(id)
            setShowZonePicker(false)
          }}
        />
      )}
      {showPositionPicker && (
        <PositionPickerModal
          vesselLengthM={study?.vesselLengthM ?? null}
          vesselBreadthM={study?.vesselBreadthM ?? null}
          initialX={parseFloat(posX) || 0}
          initialY={parseFloat(posY) || 0}
          initialHeadingDeg={selectedMachine?.system_type === 'mcg30' ? parseFloat(slewing) || 0 : parseFloat(orientation) || 0}
          headingLabel={selectedMachine?.system_type === 'mcg30' ? 'Slewing angle' : 'Orientation'}
          headingHint={
            selectedMachine?.system_type === 'mcg30'
              ? '90° = port side, 270° = starboard side'
              : selectedMachine?.system_type === 'heavy_feeder'
                ? '0° = cylinders on port side'
                : undefined
          }
          onClose={() => setShowPositionPicker(false)}
          onConfirm={(x, y, headingDeg) => {
            setPosX(String(x))
            setPosY(String(y))
            if (selectedMachine?.system_type === 'mcg30') setSlewing(String(headingDeg))
            else setOrientation(String(headingDeg))
            setShowPositionPicker(false)
          }}
        />
      )}
      {showManage && study && (
        <ManageStudyModal
          studyId={study.id}
          studyName={study.name}
          ownerName={ownerName}
          ownerEmail={ownerEmail}
          collaborators={collaborators}
          archived={archived}
          onRenamed={(name) => onNav('builder', { ...study, name })}
          onCollaboratorsChange={setCollaborators}
          onArchivedChange={setArchived}
          onTransferred={(newOwnerEmail, newOwnerName) => {
            setOwnerEmail(newOwnerEmail)
            setOwnerName(newOwnerName)
            setShowManage(false)
          }}
          onDelete={() =>
            deleteStudy(study.id)
              .then(() => onNav('dashboard'))
              .catch(() => {})
          }
          onClose={() => setShowManage(false)}
        />
      )}
    </div>
  )
}
