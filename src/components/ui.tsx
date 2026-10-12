// The app's shared look: buttons, the study top bar, panels, banners, form fields, modals and
// empty states -- so every screen is put together from the same pieces instead of each one
// hand-styling its own. Colors are the bm-* tokens from index.css (Barge Master's palette).
import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode } from 'react'
import type { StudyStatus } from '../App'
import ModalBackdrop from './ModalBackdrop'
import StatusChip from './StatusChip'

// ---- Buttons ----

type ButtonVariant = 'primary' | 'dark' | 'success' | 'outline' | 'secondary' | 'neutral' | 'danger'
type ButtonSize = 'sm' | 'md'

const BUTTON_BASE =
  'inline-flex items-center justify-center gap-1.5 font-bold rounded border whitespace-nowrap transition-colors disabled:opacity-40 disabled:cursor-not-allowed'
const BUTTON_SIZE: Record<ButtonSize, string> = { sm: 'px-3 py-1.5 text-xs', md: 'px-4 py-2 text-sm' }
const BUTTON_VARIANT: Record<ButtonVariant, string> = {
  // The main action of a screen or panel.
  primary: 'bg-bm-blue border-bm-blue text-white hover:bg-bm-blue-dark hover:border-bm-blue-dark',
  // Decisions that lock something in (approve a result, start a revision).
  dark: 'bg-bm-navy border-bm-navy text-white hover:bg-bm-navy-light hover:border-bm-navy-light',
  success: 'bg-bm-success border-bm-success text-white hover:bg-bm-success-dark hover:border-bm-success-dark',
  // Secondary actions that belong to the main flow (pickers, uploads, comments).
  outline: 'bg-white border-bm-blue text-bm-blue hover:bg-bm-tint',
  // Navigation and management (back to studies, manage, downloads).
  secondary: 'bg-white border-bm-navy text-bm-navy hover:bg-bm-navy-tint',
  // Cancel / close.
  neutral: 'bg-white border-bm-rule text-bm-navy hover:bg-bm-shade',
  danger: 'bg-white border-bm-danger text-bm-danger hover:bg-bm-danger-tint',
}

/** The class string of a button -- for <a> and <label> elements that should look like one. */
export function buttonClass(variant: ButtonVariant = 'primary', size: ButtonSize = 'md', extra = ''): string {
  return `${BUTTON_BASE} ${BUTTON_SIZE[size]} ${BUTTON_VARIANT[variant]} ${extra}`
}

export function Button({
  variant = 'primary',
  size = 'md',
  className = '',
  type = 'button',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: ButtonVariant; size?: ButtonSize }) {
  return <button type={type} className={buttonClass(variant, size, className)} {...props} />
}

/** A text-only action inside dense lists (Reply, Resolve, Show resolved). */
export function LinkButton({ className = '', type = 'button', ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button type={type} className={`text-xs font-bold text-bm-blue hover:underline disabled:opacity-40 ${className}`} {...props} />
}

/** One option of a set where one is picked (tabs, system types, loadcases, versions). */
export function choiceClass(selected: boolean, size: ButtonSize = 'md', extra = ''): string {
  return `${BUTTON_BASE} ${BUTTON_SIZE[size]} ${selected ? 'bg-bm-blue border-bm-blue text-white' : 'bg-white border-bm-rule text-bm-navy hover:border-bm-blue hover:text-bm-blue'} ${extra}`
}

// ---- Page structure ----

/** The bar along the top of every study screen: back to the list, which study, where it stands. */
export function TopBar({
  onBack,
  title,
  status,
  revision,
  meta,
  children,
}: {
  onBack: () => void
  title: string
  status?: StudyStatus
  revision?: number
  meta?: ReactNode
  children?: ReactNode
}) {
  return (
    <header className="h-14 flex-shrink-0 flex items-center gap-3 px-6 border-b border-bm-rule bg-white">
      <Button variant="secondary" size="sm" onClick={onBack}>
        ← Studies
      </Button>
      <span className="font-bold text-bm-navy truncate">{title}</span>
      {status && <StatusChip status={status} />}
      {revision !== undefined && <span className="text-xs font-bold text-bm-navy whitespace-nowrap">Rev {revision}</span>}
      {meta && <span className="text-xs text-bm-subtle truncate">{meta}</span>}
      {children && <div className="ml-auto flex items-center gap-2 flex-shrink-0">{children}</div>}
    </header>
  )
}

/** The scrolling content column of a form-like screen (setup, upload). */
export function PageBody({ children }: { children: ReactNode }) {
  return <main className="flex-1 w-full max-w-3xl mx-auto px-8 py-8">{children}</main>
}

/** A screen's own title, for the screens without a panel (the studies list). */
export function PageTitle({ title, children, actions }: { title: string; children?: ReactNode; actions?: ReactNode }) {
  return (
    <div className="flex items-end justify-between gap-4 mb-6">
      <div>
        <h1 className="text-lg font-bold uppercase tracking-wide text-bm-navy">{title}</h1>
        {children && <p className="text-sm mt-1 text-bm-muted">{children}</p>}
      </div>
      {actions}
    </div>
  )
}

/** The gray title bar of a panel or side column. */
export function PanelHeader({ title, children, description }: { title: ReactNode; children?: ReactNode; description?: ReactNode }) {
  return (
    <div className="flex-shrink-0 px-6 py-3 min-h-11 flex flex-col justify-center border-b border-bm-rule bg-bm-shade">
      <div className="flex items-center gap-2">
        <h2 className="text-xs font-bold uppercase tracking-widest text-bm-navy">{title}</h2>
        {children}
      </div>
      {description && <p className="text-sm mt-1 text-bm-muted">{description}</p>}
    </div>
  )
}

/** A white card with a gray title bar, its content, and optionally a gray footer with its actions. */
export function Panel({
  title,
  description,
  footer,
  children,
  className = '',
}: {
  title: ReactNode
  description?: ReactNode
  footer?: ReactNode
  children: ReactNode
  className?: string
}) {
  return (
    <section className={`bg-white border border-bm-rule rounded overflow-hidden ${className}`}>
      <PanelHeader title={title} description={description} />
      <div className="px-6 py-5 flex flex-col gap-6">{children}</div>
      {footer && <PanelFooter>{footer}</PanelFooter>}
    </section>
  )
}

function PanelFooter({ children }: { children: ReactNode }) {
  return <div className="px-6 py-3 flex items-center justify-end gap-2 border-t border-bm-rule bg-bm-shade">{children}</div>
}

/** A titled group of fields or content inside a panel. */
export function SectionTitle({ children, aside, hint }: { children: ReactNode; aside?: ReactNode; hint?: ReactNode }) {
  return (
    <div className="mb-3">
      <div className="flex items-center justify-between gap-2 pb-1 border-b border-bm-rule">
        <h3 className="text-xs font-bold uppercase tracking-wider text-bm-navy">{children}</h3>
        {aside}
      </div>
      {hint && <p className="text-xs mt-2 text-bm-subtle">{hint}</p>}
    </div>
  )
}

// ---- Messages ----

type Tone = 'info' | 'warning' | 'error' | 'success' | 'neutral'

const TONE: Record<Tone, string> = {
  info: 'bg-bm-tint border-bm-info-rule text-bm-info',
  warning: 'bg-bm-warning-tint border-bm-warning-rule text-bm-warning',
  error: 'bg-bm-danger-tint border-bm-danger-rule text-bm-danger-text',
  success: 'bg-bm-success-tint border-bm-success-rule text-bm-success',
  neutral: 'bg-bm-shade border-bm-rule text-bm-muted',
}

/**
 * A message in one of five tones. `bar` spans the screen under the top bar (status of the whole
 * screen); otherwise it's a box inside the content.
 */
export function Banner({
  tone,
  title,
  children,
  action,
  onDismiss,
  bar = false,
  className = '',
}: {
  tone: Tone
  title?: ReactNode
  children?: ReactNode
  action?: ReactNode
  onDismiss?: () => void
  bar?: boolean
  className?: string
}) {
  const shape = bar ? 'px-6 py-2.5 border-b flex-shrink-0' : 'px-4 py-3 border rounded'
  return (
    <div className={`${shape} ${TONE[tone]} text-sm flex items-center gap-3 ${className}`}>
      <div className="flex-1 min-w-0">
        {title && <div className="font-bold">{title}</div>}
        {children && <div className={title ? 'text-xs mt-0.5' : ''}>{children}</div>}
      </div>
      {action && <div className="flex-shrink-0">{action}</div>}
      {onDismiss && (
        <button onClick={onDismiss} aria-label="Dismiss" className="flex-shrink-0 text-xs opacity-70 hover:opacity-100">
          ✕
        </button>
      )}
    </div>
  )
}

/** A centered message filling an empty area: nothing here yet, loading, or something failed. */
export function EmptyState({ icon, title, children, action }: { icon?: ReactNode; title: ReactNode; children?: ReactNode; action?: ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center text-center h-full py-16 px-8">
      {icon && <div className="text-3xl mb-4 text-bm-rule">{icon}</div>}
      <div className="font-bold uppercase tracking-wide text-sm mb-2 text-bm-navy">{title}</div>
      {children && <div className="text-sm max-w-md text-bm-subtle">{children}</div>}
      {action && <div className="mt-5">{action}</div>}
    </div>
  )
}

export function Spinner({ className = '' }: { className?: string }) {
  return <div className={`w-8 h-8 rounded-full border-[3px] border-bm-tint border-t-bm-blue animate-spin ${className}`} />
}

/** The whole-screen state before a study screen has loaded (or when loading it failed). */
export function ScreenMessage({ error }: { error?: string | null }) {
  return (
    <div className="flex-1 flex items-center justify-center">
      {error ? <Banner tone="error" title="Could not load this study">{error}</Banner> : <Spinner />}
    </div>
  )
}

// ---- Form fields ----

export const INPUT =
  'w-full border border-bm-rule rounded bg-white px-2.5 py-1.5 text-sm text-bm-ink placeholder:text-bm-placeholder focus:outline-none focus:border-bm-blue focus:ring-2 focus:ring-bm-blue/20 disabled:bg-bm-shade disabled:text-bm-muted disabled:cursor-not-allowed'

/** A labelled field: the label above, the control, and an optional hint below. */
export function Field({ label, hint, children, className = '' }: { label: ReactNode; hint?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <label className={`block ${className}`}>
      <span className="block text-xs font-bold mb-1 text-bm-text">{label}</span>
      {children}
      {hint && <span className="block text-xs mt-1 text-bm-subtle">{hint}</span>}
    </label>
  )
}

/** A number (or other) input with its unit shown at its right edge. */
export function UnitInput({ unit, className = '', ...props }: InputHTMLAttributes<HTMLInputElement> & { unit: string }) {
  return (
    <div className="flex items-stretch border border-bm-rule rounded overflow-hidden bg-white focus-within:border-bm-blue focus-within:ring-2 focus-within:ring-bm-blue/20">
      <input className={`flex-1 min-w-0 px-2.5 py-1.5 text-sm text-bm-ink bg-transparent focus:outline-none ${className}`} {...props} />
      <span className="px-2 flex items-center text-xs border-l border-bm-rule bg-bm-shade text-bm-subtle">{unit}</span>
    </div>
  )
}

/** Side-by-side number fields in one unit (X/Y/Z, Tp min/max/step); `className` sets the grid's columns and gap. */
export function UnitFieldGrid({
  unit,
  fields,
  className,
}: {
  unit: string
  fields: [label: string, value: string, onChange: (value: string) => void][]
  className: string
}) {
  return (
    <div className={`grid ${className}`}>
      {fields.map(([label, value, onChange]) => (
        <Field key={label} label={label}>
          <UnitInput unit={unit} type="number" value={value} onChange={(e) => onChange(e.target.value)} />
        </Field>
      ))}
    </div>
  )
}

// ---- Modals ----

/** A popup: navy title bar with a close button, the content, and a gray footer for its actions. */
export function Modal({
  title,
  subtitle,
  width,
  onClose,
  footer,
  children,
}: {
  title: ReactNode
  subtitle?: ReactNode
  width: number
  onClose: () => void
  footer?: ReactNode
  children: ReactNode
}) {
  return (
    <ModalBackdrop onClose={onClose}>
      <div className="rounded shadow-lg overflow-hidden bg-white" style={{ width, maxWidth: '100%' }}>
        <div className="px-5 py-3 flex items-center justify-between gap-4 bg-bm-navy">
          <div className="min-w-0">
            <div className="text-white font-bold text-sm uppercase tracking-wide">{title}</div>
            {subtitle && <div className="text-white/60 text-xs mt-0.5">{subtitle}</div>}
          </div>
          <button
            onClick={onClose}
            aria-label="Close"
            className="w-7 h-7 flex-shrink-0 flex items-center justify-center rounded border border-white/40 text-white text-lg leading-none transition-colors hover:bg-white/10"
          >
            ×
          </button>
        </div>
        {children}
        {footer && <div className="px-5 py-3 flex items-center justify-between gap-3 border-t border-bm-rule bg-bm-shade">{footer}</div>}
      </div>
    </ModalBackdrop>
  )
}

// ---- Tables ----

export const TABLE_HEAD_CELL = 'px-4 py-2.5 text-left text-xs font-bold uppercase tracking-wider text-bm-navy bg-bm-shade border-b border-bm-rule'
export const TABLE_CELL = 'px-4 py-3'
