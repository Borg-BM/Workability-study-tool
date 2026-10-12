// The choices a report document is generated from: header fields and which uploaded images
// fill the figure slots. Shown before the first generation, and again for "Regenerate".
import { useState } from 'react'
import { API_BASE, type ApiStudyDetail } from '../api'
import type { ReportHeader, ReportState } from '../reportModel'
import { Banner, Button, Field, INPUT, Panel, SectionTitle } from './ui'

// Author and Check aren't typed in: Author is whoever generates the document, Check the
// reviewer it's submitted to (see backend/app/routers/studies.py) -- shown disabled below.
const HEADER_FIELDS: { field: keyof ReportHeader; label: string; placeholder?: string; wide?: boolean }[] = [
  { field: 'subject', label: 'Subject', wide: true },
  { field: 'project', label: 'Project' },
  { field: 'ref', label: 'Ref.', placeholder: 'BM-OPXXXX-EN-XXXX-Rev0' },
  { field: 'date', label: 'Date' },
]

interface ReportSetupProps {
  detail: ApiStudyDetail
  initial: ReportState
  authorName: string
  regenerate: boolean
  busy: boolean
  error: string | null
  onGenerate: (report: ReportState) => void
  onCancel?: () => void
}

export default function ReportSetup({ detail, initial, authorName, regenerate, busy, error, onGenerate, onCancel }: ReportSetupProps) {
  const [draft, setDraft] = useState(initial)
  const images = detail.files.filter((f) => f.kind === 'image')
  const approved = detail.versions.find((v) => v.approved) || null

  const setHeader = (field: keyof ReportHeader, value: string) => setDraft((d) => ({ ...d, header: { ...d.header, [field]: value } }))
  const toggleAdditional = (id: string) =>
    setDraft((d) => ({
      ...d,
      additional_figure_ids: d.additional_figure_ids.includes(id) ? d.additional_figure_ids.filter((x) => x !== id) : [...d.additional_figure_ids, id],
    }))

  const figureSelect = (label: string, value: string | null, onChange: (id: string | null) => void, emptyLabel = '— leave a placeholder —') => (
    <Field label={label}>
      <select className={INPUT} value={value || ''} onChange={(e) => onChange(e.target.value || null)}>
        <option value="">{emptyLabel}</option>
        {images.map((f) => (
          <option key={f.id} value={f.id}>
            {f.caption || f.original_filename}
          </option>
        ))}
      </select>
    </Field>
  )

  return (
    <Panel
      title={regenerate ? 'Regenerate report' : 'Set up the report'}
      description="This builds a Word document in Barge Master's report style. After that you write and edit the report in the document itself — or download it and carry on in Word."
      footer={
        <>
          {onCancel && (
            <Button variant="neutral" onClick={onCancel} disabled={busy}>
              Cancel
            </Button>
          )}
          <Button onClick={() => onGenerate(draft)} disabled={busy}>
            {busy ? 'Generating…' : regenerate ? 'Regenerate report' : 'Generate report'}
          </Button>
        </>
      }
    >
      <Banner tone={approved ? 'info' : 'warning'}>
        {approved
          ? `The overview of results, the input parameters, the workability figures and Appendix A come from the approved result, ${approved.label}.`
          : 'No approved result yet — the results, input parameters and Appendix A will be placeholders until you approve one in Build study and regenerate.'}
      </Banner>

      <section>
        <SectionTitle>Title block</SectionTitle>
        <div className="grid grid-cols-2 gap-x-4 gap-y-3">
          {HEADER_FIELDS.map(({ field, label, placeholder, wide }) => (
            <Field key={field} label={label} className={wide ? 'col-span-2' : ''}>
              <input className={INPUT} value={draft.header[field]} placeholder={placeholder} onChange={(e) => setHeader(field, e.target.value)} />
            </Field>
          ))}
          <Field label="Author">
            <input className={INPUT} value={authorName} disabled />
          </Field>
          <Field label="Check / Approval">
            <input className={INPUT} value="" placeholder="The reviewer, filled in on submission" disabled />
          </Field>
        </div>
      </section>

      <section>
        <SectionTitle>Figures</SectionTitle>
        {images.length === 0 ? (
          <p className="text-xs text-bm-subtle">No images uploaded — add some on the Upload material step, or insert pictures into the document later.</p>
        ) : (
          <div className="flex flex-col gap-3">
            <div className="grid grid-cols-2 gap-4">
              {figureSelect('General arrangement (chapter 3)', draft.concept_drawing_file_id, (id) => setDraft((d) => ({ ...d, concept_drawing_file_id: id })))}
              {figureSelect('Figure 1: Axis convention', draft.axis_convention_file_id, (id) => setDraft((d) => ({ ...d, axis_convention_file_id: id })), '— BM standard diagram —')}
            </div>
            <div>
              <span className="block text-xs font-bold mb-1 text-bm-text">Additional figures</span>
              <div className="flex flex-wrap gap-3">
                {images.map((f) => {
                  const selected = draft.additional_figure_ids.includes(f.id)
                  return (
                    <button
                      key={f.id}
                      type="button"
                      onClick={() => toggleAdditional(f.id)}
                      className={`w-28 border-2 rounded overflow-hidden text-left transition-colors ${selected ? 'border-bm-blue' : 'border-bm-rule hover:border-bm-blue'}`}
                    >
                      <img src={`${API_BASE}${f.url}`} alt={f.caption || f.original_filename} className="w-full h-16 object-cover" />
                      <div className={`px-1.5 py-1 text-xs truncate ${selected ? 'font-bold text-bm-blue' : 'text-bm-muted'}`}>{f.caption || f.original_filename}</div>
                    </button>
                  )
                })}
              </div>
            </div>
          </div>
        )}
      </section>

      {regenerate && (
        <Banner tone="error">This replaces the current document — anything written or changed in it will be lost. Download a copy first if you want to keep it.</Banner>
      )}
      {error && <Banner tone="error">{error}</Banner>}
    </Panel>
  )
}
