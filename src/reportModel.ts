// The choices a study's report document is generated from (backend/app/report_docx.py) -- header
// fields and which uploads fill which figure slot. The report text itself lives in the generated
// .docx, not here. Author, Check and Approval aren't choices: the backend fills them in (whoever
// generates the document, and the reviewer it's submitted to).
import type { Study } from './App'

export interface ReportHeader {
  subject: string
  project: string
  ref: string
  date: string
}

export interface ReportState {
  header: ReportHeader
  concept_drawing_file_id: string | null
  axis_convention_file_id: string | null
  additional_figure_ids: string[]
}

// Kept in step with SYSTEM_LABELS in backend/app/report_docx.py, which makes the same default subject.
export const SYSTEM_LABELS: Record<string, string> = {
  mcg30: 'BM-MCG',
  t700: 'BM-T700',
  heavy_feeder: 'BM-HF',
}

function todayDDMMYYYY(): string {
  const d = new Date()
  return `${d.getDate()}-${d.getMonth() + 1}-${d.getFullYear()}`
}

export function defaultReport(study: Study, systemLabel: string): ReportState {
  return {
    header: {
      subject: `Workability report of the ${systemLabel} onboard the ${study.vessel || '[vessel]'}`,
      project: study.project || '',
      ref: '',
      date: todayDDMMYYYY(),
    },
    concept_drawing_file_id: null,
    axis_convention_file_id: null,
    additional_figure_ids: [],
  }
}

// A saved report over the defaults, so a field added since it was saved still has a value.
export function mergeReport(defaults: ReportState, saved: Record<string, unknown>): ReportState {
  const savedHeader = (saved.header as Partial<ReportHeader>) || {}
  return {
    ...defaults,
    ...saved,
    header: { ...defaults.header, ...savedHeader },
  } as ReportState
}
