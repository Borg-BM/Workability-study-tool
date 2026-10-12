// "1. Build study" step 0, effectively: names the study, picks its one vessel/loadcase
// RAO (which locks in permanently -- see handleContinue below and db.set_study_rao on the
// backend), and optionally records vessel dimensions for the eventual report. Only reachable
// for a study that doesn't have a vessel yet (App.tsx's openStudy sends anything else
// straight to StudyBuilder instead).
import { useEffect, useMemo, useState } from 'react'
import type { Study, Screen } from '../App'
import Stepper from '../components/Stepper'
import { Banner, Button, Field, INPUT, PageBody, Panel, SectionTitle, TopBar, UnitFieldGrid, choiceClass } from '../components/ui'
import { errorMessage, type ApiSystemType, listVessels, listLoadcases, listSystemTypes, setStudyRao, updateStudy } from '../api'

export default function StudySetup({ study, onNav }: { study: Study | null; onNav: (s: Screen, study?: Study) => void }) {
  const [name, setName] = useState(study?.name || '')
  const [project, setProject] = useState(study?.project || '')

  const [systemTypes, setSystemTypes] = useState<ApiSystemType[]>([])
  const [pickedSystemType, setPickedSystemType] = useState<string | null>(null)

  const [vessels, setVessels] = useState<string[]>([])
  const [vesselsError, setVesselsError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [pickedVessel, setPickedVessel] = useState<string | null>(null)
  const [loadcases, setLoadcases] = useState<string[]>([])
  const [pickedLoadcase, setPickedLoadcase] = useState<string | null>(null)

  const [length, setLength] = useState('')
  const [breadth, setBreadth] = useState('')
  const [depth, setDepth] = useState('')
  const [draft, setDraft] = useState('')

  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listVessels()
      .then(({ vessels }) => setVessels(vessels))
      .catch((err) => setVesselsError(err.message || 'Could not reach the backend'))
    listSystemTypes().then(({ system_types }) => setSystemTypes(system_types)).catch(() => {})
  }, [])

  const filteredVessels = useMemo(
    () => vessels.filter((v) => v.toLowerCase().includes(search.toLowerCase())),
    [vessels, search]
  )

  // Loadcases depend on which vessel is picked, so they're fetched fresh (and the old
  // selection cleared) on every vessel pick, not derived/filtered client-side.
  const pickVessel = (vessel: string) => {
    setPickedVessel(vessel)
    setPickedLoadcase(null)
    setLoadcases([])
    listLoadcases(vessel)
      .then(({ loadcases }) => setLoadcases(loadcases))
      .catch(() => setLoadcases([]))
  }

  const canContinue = Boolean(pickedVessel && pickedLoadcase && pickedSystemType) && !submitting

  // Two sequential API calls, not one: updateStudy saves the name/project (which can be
  // edited any time), then setStudyRao locks in the vessel/loadcase + dimensions
  // (permanently -- see its backend docstring). Both must succeed before navigating on;
  // if setStudyRao fails after updateStudy already succeeded, the name/project change is
  // still saved (no rollback), which is fine since that half has no "only once" constraint.
  // The merged Study object passed to onNav is built by hand from `study` + both
  // responses, rather than re-fetching the study, so StudyBuilder can render immediately
  // with the just-saved values instead of waiting on another round trip.
  const handleContinue = async () => {
    if (!study || !pickedVessel || !pickedLoadcase || !pickedSystemType) return
    setSubmitting(true)
    setError(null)
    try {
      await updateStudy(study.id, { name: name || undefined, project })
      const updated = await setStudyRao(study.id, pickedVessel, pickedLoadcase, pickedSystemType, {
        vessel_length_m: length ? parseFloat(length) : null,
        vessel_breadth_m: breadth ? parseFloat(breadth) : null,
        vessel_depth_m: depth ? parseFloat(depth) : null,
        vessel_draft_m: draft ? parseFloat(draft) : null,
      })
      onNav('builder', {
        ...study,
        name: name || study.name,
        project,
        vessel: updated.vessel,
        loadcase: updated.loadcase,
        systemType: updated.system_type,
        vesselLengthM: updated.vessel_length_m,
        vesselBreadthM: updated.vessel_breadth_m,
        vesselDepthM: updated.vessel_depth_m,
        vesselDraftM: updated.vessel_draft_m,
      })
    } catch (err) {
      setError(errorMessage(err, 'Could not save study setup'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-bm-shade">
      <Stepper screen="setup" status="draft" onNav={onNav} />
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar onBack={() => onNav('dashboard')} title={study?.name || 'New study'} status="draft" />

        <PageBody>
          <Panel
            title="Study setup"
            description="A study covers exactly one vessel. Set it up once here — you won't be able to change the vessel later (delete the study and start over instead)."
            footer={
              <Button onClick={handleContinue} disabled={!canContinue}>
                {submitting ? 'Saving…' : 'Continue to parameters →'}
              </Button>
            }
          >
            {error && <Banner tone="error">{error}</Banner>}

            <section>
              <SectionTitle>Study details</SectionTitle>
              <div className="grid grid-cols-2 gap-4">
                <Field label="Study reference">
                  <input className={INPUT} value={name} onChange={(e) => setName(e.target.value)} placeholder="WS-2026-001" />
                </Field>
                <Field label="Project">
                  <input className={INPUT} value={project} onChange={(e) => setProject(e.target.value)} placeholder="e.g. OP1180" />
                </Field>
              </div>
            </section>

            <section>
              <SectionTitle hint="Fixed for the life of the study — the Study Builder will only offer machine variants of this type.">1. System type</SectionTitle>
              <div className="flex gap-2 flex-wrap">
                {systemTypes.map((st) => (
                  <button key={st.id} onClick={() => setPickedSystemType(st.id)} className={choiceClass(pickedSystemType === st.id)}>
                    {st.label}
                  </button>
                ))}
              </div>
            </section>

            <section>
              <SectionTitle>2. RAO</SectionTitle>
              <input className={`${INPUT} mb-3`} placeholder="Search vessel name…" value={search} onChange={(e) => setSearch(e.target.value)} />
              <div className="border border-bm-rule rounded flex bg-white" style={{ minHeight: 220 }}>
                <div className="w-1/2 border-r border-bm-rule overflow-y-auto" style={{ maxHeight: 260 }}>
                  {vesselsError ? (
                    <p className="p-4 text-xs text-bm-danger-text">Could not reach the backend: {vesselsError}</p>
                  ) : filteredVessels.length === 0 ? (
                    <p className="p-4 text-xs text-bm-subtle">No vessels match.</p>
                  ) : (
                    filteredVessels.map((v) => (
                      <button
                        key={v}
                        onClick={() => pickVessel(v)}
                        className={`w-full text-left px-3 py-2 text-sm border-b border-bm-rule-light text-bm-navy transition-colors ${pickedVessel === v ? 'bg-bm-tint font-bold' : 'hover:bg-bm-shade'}`}
                      >
                        {v}
                      </button>
                    ))
                  )}
                </div>
                <div className="w-1/2 overflow-y-auto p-3" style={{ maxHeight: 260 }}>
                  {!pickedVessel ? (
                    <p className="text-xs text-bm-subtle">Pick a vessel to see its loadcases.</p>
                  ) : loadcases.length === 0 ? (
                    <p className="text-xs text-bm-subtle">Loading loadcases…</p>
                  ) : (
                    <div className="flex flex-col gap-1.5">
                      {loadcases.map((lc) => (
                        <button key={lc} onClick={() => setPickedLoadcase(lc)} className={choiceClass(pickedLoadcase === lc, 'md', 'justify-start!')}>
                          {lc}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
              {pickedVessel && pickedLoadcase && (
                <p className="text-xs mt-2 font-bold text-bm-success">
                  ✓ {pickedVessel} — {pickedLoadcase}
                </p>
              )}
            </section>

            <section>
              <SectionTitle hint="Not part of the RAO record — fill in if known, for reference in the eventual report.">Vessel dimensions (optional)</SectionTitle>
              <UnitFieldGrid
                unit="m"
                className="grid-cols-4 gap-3"
                fields={[
                  ['Length', length, setLength],
                  ['Breadth', breadth, setBreadth],
                  ['Depth', depth, setDepth],
                  ['Draft', draft, setDraft],
                ]}
              />
            </section>
          </Panel>
        </PageBody>
      </div>
    </div>
  )
}
