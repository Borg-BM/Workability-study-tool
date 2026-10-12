// Top-down visual picker for a system's position + heading on the vessel -- integrated
// the same way as the weather-data map pickers (LocationPickerModal, WeibullZonePickerModal,
// NdbcBuoyPickerModal): a modal opened from a button, confirming values back into
// StudyBuilder's existing X/Y/heading form fields, nothing new persisted here.
//
// Coordinate convention (matches the app's "w.r.t. APP/CL/K" position fields and PyBM's
// own slewing convention -- see MCG30_Linear's pos_tip trig, where slew=0 points +X,
// slew=90 points +Y and is documented as "port side"): +X = toward the bow, measured from
// the aft perpendicular (X=0 at AP, X=length at the bow), +Y = toward port from the
// centerline. This component draws the vessel with the bow at the top of the canvas, so
// port ends up on the left and starboard on the right -- a standard top-down chart view.
import { useRef, useState } from 'react'
import { Banner, Button, Field, Modal, UnitInput } from './ui'

interface Props {
  vesselLengthM: number | null
  vesselBreadthM: number | null
  initialX: number
  initialY: number
  initialHeadingDeg: number
  headingLabel: string
  headingHint?: string
  onConfirm: (x: number, y: number, headingDeg: number) => void
  onClose: () => void
}

const VIEW_W = 440
const VIEW_H = 560
const MARGIN = 44
const DEFAULT_LENGTH_M = 80
const DEFAULT_BREADTH_M = 20
const ARROW_LEN_PX = 46

function toRad(deg: number) {
  return (deg * Math.PI) / 180
}

// theta=0 -> screen "up" (bow); theta=90 -> screen "left" (port); theta=270 -> "right"
// (starboard) -- see the file header comment for the full derivation.
function headingToScreenDelta(headingDeg: number, len: number) {
  const t = toRad(headingDeg)
  return { dx: -Math.sin(t) * len, dy: -Math.cos(t) * len }
}

function screenDeltaToHeading(dx: number, dy: number) {
  const deg = (Math.atan2(-dx, -dy) * 180) / Math.PI
  return (deg + 360) % 360
}

// Smallest 1/2/5 x 10^n step giving roughly `target` ticks over `span` meters.
function niceTickStep(span: number, target = 6) {
  const raw = span / target
  const pow = 10 ** Math.floor(Math.log10(raw))
  return ([1, 2, 5, 10].find((m) => m * pow >= raw) ?? 10) * pow
}

export default function PositionPickerModal({
  vesselLengthM,
  vesselBreadthM,
  initialX,
  initialY,
  initialHeadingDeg,
  headingLabel,
  headingHint,
  onConfirm,
  onClose,
}: Props) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [x, setX] = useState(initialX)
  const [y, setY] = useState(initialY)
  const [heading, setHeading] = useState(initialHeadingDeg)
  const [dragging, setDragging] = useState<'marker' | 'heading' | null>(null)

  const lengthM = vesselLengthM && vesselLengthM > 0 ? vesselLengthM : DEFAULT_LENGTH_M
  const breadthM = vesselBreadthM && vesselBreadthM > 0 ? vesselBreadthM : DEFAULT_BREADTH_M
  const usingPlaceholderDims = !(vesselLengthM && vesselLengthM > 0) || !(vesselBreadthM && vesselBreadthM > 0)

  // Fit the vessel hull (AP at X=0 to the bow at X=length) *and* the current marker
  // position inside the drawing area -- a machine placed beyond the hull (e.g. an
  // over-water crane reach) should still show up rather than clip, since seeing that is
  // exactly the kind of thing this visual is for.
  const xMin = Math.min(0, x)
  const xMax = Math.max(lengthM, x)
  const xMid = (xMin + xMax) / 2
  const extentX = ((xMax - xMin) / 2) * 1.2
  const extentY = Math.max(breadthM / 2, Math.abs(y)) * 1.2
  const scale = Math.min((VIEW_H - 2 * MARGIN) / (2 * extentX), (VIEW_W - 2 * MARGIN) / (2 * extentY))
  const centerX = VIEW_W / 2
  const centerY = VIEW_H / 2

  const vesselToScreen = (vx: number, vy: number) => ({ sx: centerX - vy * scale, sy: centerY - (vx - xMid) * scale })
  const screenToVessel = (sx: number, sy: number) => ({ vx: xMid + (centerY - sy) / scale, vy: (centerX - sx) / scale })

  const marker = vesselToScreen(x, y)
  const { dx: arrowDx, dy: arrowDy } = headingToScreenDelta(heading, ARROW_LEN_PX)
  const arrowTip = { sx: marker.sx + arrowDx, sy: marker.sy + arrowDy }

  // Bow-pointed hull outline (a rectangle with a tapered bow), drawn in vessel-frame
  // meters then projected through vesselToScreen -- matches PyBM's own plot_ship()
  // convention of a bow-pointed hull shape, just oriented bow-up instead of bow-right.
  const halfB = breadthM / 2
  const bowTaper = lengthM * 0.075
  const hullPoints = [
    [lengthM, 0],
    [lengthM - bowTaper, halfB],
    [0, halfB],
    [0, -halfB],
    [lengthM - bowTaper, -halfB],
  ]
    .map(([vx, vy]) => vesselToScreen(vx, vy))
    .map((p) => `${p.sx},${p.sy}`)
    .join(' ')

  // X ruler along the starboard side, counting forward from AP.
  const tickStep = niceTickStep(xMax - xMin)
  const ticks: number[] = []
  for (let t = Math.ceil(xMin / tickStep) * tickStep; t <= xMax + 1e-9; t += tickStep) ticks.push(t)
  const hullPortSx = vesselToScreen(0, halfB).sx
  const hullStbdSx = vesselToScreen(0, -halfB).sx
  const apSy = vesselToScreen(0, 0).sy

  const svgPoint = (clientX: number, clientY: number) => {
    const rect = svgRef.current?.getBoundingClientRect()
    if (!rect) return { sx: 0, sy: 0 }
    return {
      sx: ((clientX - rect.left) / rect.width) * VIEW_W,
      sy: ((clientY - rect.top) / rect.height) * VIEW_H,
    }
  }

  const handlePointerMove = (e: React.PointerEvent<SVGSVGElement>) => {
    if (!dragging) return
    const { sx, sy } = svgPoint(e.clientX, e.clientY)
    if (dragging === 'marker') {
      const { vx, vy } = screenToVessel(sx, sy)
      setX(Math.round(vx * 100) / 100)
      setY(Math.round(vy * 100) / 100)
    } else {
      setHeading(Math.round(screenDeltaToHeading(sx - marker.sx, sy - marker.sy)))
    }
  }

  const startDrag = (which: 'marker' | 'heading') => (e: React.PointerEvent) => {
    e.stopPropagation()
    ;(e.target as Element).setPointerCapture(e.pointerId)
    setDragging(which)
  }

  return (
    <Modal
      title="Position & heading on ship"
      subtitle="Top-down view — drag the marker to move it, drag the arrow tip to set heading"
      width={720}
      onClose={onClose}
      footer={
        <div className="ml-auto flex gap-2">
          <Button variant="neutral" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={() => onConfirm(x, y, heading)}>Use this position & heading</Button>
        </div>
      }
    >
        <div className="flex">
          <svg
            ref={svgRef}
            width={VIEW_W}
            height={VIEW_H}
            viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
            style={{ background: '#F5F5F3', touchAction: 'none', cursor: dragging ? 'grabbing' : 'default' }}
            onPointerMove={handlePointerMove}
            onPointerUp={() => setDragging(null)}
            onClick={(e) => {
              if (dragging) return
              const { sx, sy } = svgPoint(e.clientX, e.clientY)
              const { vx, vy } = screenToVessel(sx, sy)
              setX(Math.round(vx * 100) / 100)
              setY(Math.round(vy * 100) / 100)
            }}
          >
            {/* Bow / stern / port / starboard labels */}
            <text x={centerX} y={MARGIN - 20} textAnchor="middle" fontSize="11" fontWeight="bold" fill="#888">BOW</text>
            <text x={centerX} y={VIEW_H - MARGIN + 32} textAnchor="middle" fontSize="11" fontWeight="bold" fill="#888">STERN</text>
            <text x={MARGIN - 28} y={centerY} textAnchor="middle" fontSize="11" fontWeight="bold" fill="#888" transform={`rotate(-90 ${MARGIN - 28} ${centerY})`}>PORT</text>
            <text x={VIEW_W - MARGIN + 28} y={centerY} textAnchor="middle" fontSize="11" fontWeight="bold" fill="#888" transform={`rotate(90 ${VIEW_W - MARGIN + 28} ${centerY})`}>STARBOARD</text>

            <polygon points={hullPoints} fill="#E6F7FD" stroke="#00ADEF" strokeWidth={2} />
            {/* Centerline */}
            <line
              x1={vesselToScreen(0, 0).sx} y1={vesselToScreen(0, 0).sy}
              x2={vesselToScreen(lengthM, 0).sx} y2={vesselToScreen(lengthM, 0).sy}
              stroke="#00ADEF" strokeWidth={1} strokeDasharray="3,3" opacity={0.5}
            />

            {/* Aft perpendicular -- the X origin */}
            <line x1={hullPortSx - 10} y1={apSy} x2={hullStbdSx + 10} y2={apSy} stroke="#051642" strokeWidth={1.5} />
            <text x={hullPortSx - 14} y={apSy + 4} textAnchor="end" fontSize="11" fontWeight="bold" fill="#051642">AP (X = 0)</text>

            {/* X ruler, meters forward of AP */}
            {ticks.map((t) => {
              const sy = vesselToScreen(t, 0).sy
              return (
                <g key={t}>
                  <line x1={hullStbdSx + 4} y1={sy} x2={hullStbdSx + 10} y2={sy} stroke="#888" strokeWidth={1} />
                  <text x={hullStbdSx + 14} y={sy + 3.5} fontSize="10" fill="#888">{t} m</text>
                </g>
              )
            })}

            {/* Heading arrow */}
            <line x1={marker.sx} y1={marker.sy} x2={arrowTip.sx} y2={arrowTip.sy} stroke="#051642" strokeWidth={3} />
            <circle
              cx={arrowTip.sx} cy={arrowTip.sy} r={9}
              fill="#051642" stroke="#fff" strokeWidth={2}
              style={{ cursor: 'grab' }}
              onPointerDown={startDrag('heading')}
            />

            {/* Position marker */}
            <circle
              cx={marker.sx} cy={marker.sy} r={10}
              fill="#00ADEF" stroke="#051642" strokeWidth={2}
              style={{ cursor: 'grab' }}
              onPointerDown={startDrag('marker')}
            />
          </svg>
          <div className="flex-1 p-5 flex flex-col gap-4 bg-white">
            {usingPlaceholderDims && (
              <Banner tone="warning" className="text-xs">
                Using placeholder hull dimensions ({DEFAULT_LENGTH_M}m × {DEFAULT_BREADTH_M}m) — no vessel length/breadth on record for this study.
              </Banner>
            )}
            <div className="grid grid-cols-2 gap-3">
              <Field label="X (fwd of AP)">
                <UnitInput unit="m" type="number" value={x} onChange={(e) => setX(parseFloat(e.target.value) || 0)} />
              </Field>
              <Field label="Y (+port)">
                <UnitInput unit="m" type="number" value={y} onChange={(e) => setY(parseFloat(e.target.value) || 0)} />
              </Field>
            </div>
            <Field label={headingLabel} hint={headingHint}>
              <UnitInput unit="deg" type="number" value={heading} onChange={(e) => setHeading((((parseFloat(e.target.value) || 0) % 360) + 360) % 360)} />
            </Field>
            <p className="text-xs text-bm-subtle">Z (height) and luffing angle (if applicable) stay in the parameter form — this view is top-down only.</p>
          </div>
        </div>
    </Modal>
  )
}
