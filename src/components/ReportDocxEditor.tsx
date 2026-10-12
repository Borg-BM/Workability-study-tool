// The report document in eigenpal's Word-style docx-editor -- editable on "Generate report",
// read-only on "Review & send". Its File menu is the document toolbar: Open (upload a .docx),
// Save, Download .docx, and Export > PDF / Print, which use our own backend converter through
// the editor's `exporters` hook (docx-editor's packaged converter is paid).
import { forwardRef, useMemo } from 'react'
import { DocxEditor, useFonts, type DocxEditorRef, type Editor } from '@docx-editor.dev/react'
import { packagedFonts } from '@docx-editor.dev/fonts'
import '@docx-editor.dev/core/styles/editor.css'
import { convertDocxToPdf } from '../api'

// Metric-compatible stand-ins for Calibri/Arial etc., so line and page breaks match Word.
const FONTS = packagedFonts()

const EXPORTERS = { pdf: async (source: Uint8Array) => ({ bytes: await convertDocxToPdf(new Uint8Array(source)) }) }

// docx-editor closes its menu after its own rows via an internal context; for a host row,
// Escape on the open panel is the way out it does expose.
function closeOpenMenu() {
  document.querySelector('.docx-menubar [role="menu"]')?.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
}

interface ReportDocxEditorProps {
  docx: Uint8Array
  // Names exported PDFs; the editor would otherwise name them after its (hidden) title.
  fileName: string
  editable: boolean
  onDownload: () => void
  onEdit?: () => void
  onSave?: () => void
  onOpen?: () => void
  // The engine instance once the document is laid out -- what ReviewComments reads the
  // selection from and scrolls to comments with. Fires again after a remount.
  onReady?: (editor: Editor) => void
}

const ReportDocxEditor = forwardRef<DocxEditorRef, ReportDocxEditorProps>(function ReportDocxEditor(
  { docx, fileName, editable, onDownload, onEdit, onSave, onOpen, onReady },
  ref
) {
  const fonts = useFonts(FONTS)
  const menu = useMemo(
    () => ({
      reportIssue: false,
      exporters: EXPORTERS,
      fileName,
      children: [
        <DocxEditor.Menu.File key="file">
          {/* No Markdown converter is wired up; a read-only view has nothing to open or save. */}
          <DocxEditor.Menu.ExportMarkdown hidden />
          {!editable && <DocxEditor.Menu.Open hidden />}
          {!editable && <DocxEditor.Menu.Save hidden />}
          <DocxEditor.Menu.Row
            onSelect={() => {
              closeOpenMenu()
              onDownload()
            }}
          >
            Download .docx
          </DocxEditor.Menu.Row>
        </DocxEditor.Menu.File>,
        // Its comments and tracked changes are the paid review module; review comments are
        // our own (ReviewComments), beside the document. index.css hides the toolbar's button.
        <DocxEditor.Menu.Review key="review" hidden />,
      ],
    }),
    [fileName, editable, onDownload]
  )
  return (
    <DocxEditor
      ref={ref}
      document={docx}
      fonts={fonts}
      // Empty rather than omitted, which would show "Untitled": hides the file name.
      title=""
      mode={editable ? 'edit' : 'view'}
      menu={menu}
      // `source` is set for loads/refreshes, absent for real edits.
      onChange={onEdit ? (change) => !change.source && onEdit() : undefined}
      onSave={onSave}
      onOpen={onOpen}
      onReady={onReady}
    />
  )
})

export default ReportDocxEditor

export function reportFileName(studyName: string): string {
  return `${studyName} - Workability report`.replace(/[\\/:*?"<>|]/g, '_')
}

export function downloadFile(bytes: Uint8Array<ArrayBuffer>, fileName: string, type: string) {
  const url = URL.createObjectURL(new Blob([bytes], { type }))
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
