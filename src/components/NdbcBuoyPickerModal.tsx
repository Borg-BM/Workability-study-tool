// Map picker for a real NOAA NDBC buoy -- unlike the DNV zone picker's fixed rectangles
// (weibull_locations.py is static, so /api/locations answers instantly), the buoy list
// behind this one can take up to a minute on a cold backend cache (see
// pybm_service.list_ndbc_buoys for why: it cross-checks every buoy-type station's
// historical wave record, ~300+ of them). That slow, asynchronous arrival is the whole
// reason this component's two effects below are split the way they are -- see the comment
// on the second one.
import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { ApiBuoy } from '../api'
import { Button, Modal } from './ui'

interface Props {
  buoys: ApiBuoy[]
  initialBuoyId?: string | null
  onConfirm: (buoyId: string) => void
  onClose: () => void
}

// Collapses a sorted-with-gaps year list into a compact "1982–2013, 2015–2025" string
// (matching a real buoy's actual coverage, gaps and all -- e.g. buoy 44008 is missing
// 2014). Walks the sorted years once, closing out the current run whenever the next year
// isn't exactly `prev + 1`, including one final flush after the loop (the `i <=
// sorted.length` bound intentionally runs one iteration past the last real index, with
// `y` undefined on that pass, purely to trigger that last flush).
function yearRanges(years: number[]): string {
  if (years.length === 0) return ''
  const sorted = [...years].sort((a, b) => a - b)
  const ranges: string[] = []
  let start = sorted[0]
  let prev = sorted[0]
  for (let i = 1; i <= sorted.length; i++) {
    const y = sorted[i]
    if (y === prev + 1) {
      prev = y
      continue
    }
    ranges.push(start === prev ? `${start}` : `${start}–${prev}`)
    if (y !== undefined) {
      start = y
      prev = y
    }
  }
  return ranges.join(', ')
}

function buoyLabel(b: ApiBuoy) {
  const base = b.name ? `${b.id} — ${b.name}` : b.id
  return `${base} (${yearRanges(b.years)})`
}

export default function NdbcBuoyPickerModal({ buoys, initialBuoyId, onConfirm, onClose }: Props) {
  const mapDivRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const markerRef = useRef<Map<string, L.CircleMarker>>(new Map())
  const [hoveredId, setHoveredId] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(initialBuoyId ?? null)

  // Mount-once: just the Leaflet map + tile layer, nothing that depends on `buoys`.
  // `preferCanvas: true` renders markers to a single <canvas> instead of one <svg><path>
  // per marker -- meaningfully faster with ~150-450 markers, but means they won't show up
  // to DOM-based tooling (e.g. a test querying `path.leaflet-interactive`) even though
  // they render and are clickable just fine for a real user.
  useEffect(() => {
    if (!mapDivRef.current || mapRef.current) return
    const map = L.map(mapDivRef.current, { worldCopyJump: false, preferCanvas: true }).setView([20, -40], 2)
    mapRef.current = map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 10,
      minZoom: 2,
    }).addTo(map)

    setTimeout(() => map.invalidateSize(), 50)

    return () => {
      map.remove()
      mapRef.current = null
      markerRef.current.clear()
    }
  }, [])

  // Separate from map init: `buoys` often arrives well after the map mounts (the
  // historical-coverage check behind it is slow on a cold cache), so the markers follow the
  // prop -- a mount-once effect would leave the map blank if the modal opened first.
  useEffect(() => {
    const map = mapRef.current
    if (!map) return

    markerRef.current.forEach((marker) => map.removeLayer(marker))
    markerRef.current.clear()

    buoys.forEach((b) => {
      const marker = L.circleMarker([b.lat, b.lon], {
        radius: 5,
        color: '#00ADEF',
        weight: 1,
        fillColor: '#00ADEF',
        fillOpacity: b.id === selectedId ? 0.9 : 0.5,
      }).addTo(map)

      marker.on('mouseover', () => setHoveredId(b.id))
      marker.on('mouseout', () => setHoveredId((h) => (h === b.id ? null : h)))
      marker.on('click', () => setSelectedId(b.id))
      marker.bindTooltip(buoyLabel(b), { sticky: true })

      markerRef.current.set(b.id, marker)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [buoys])

  // Keeps marker size/opacity in sync with hover/select state without redrawing them.
  useEffect(() => {
    markerRef.current.forEach((marker, id) => {
      const active = id === selectedId
      const hovered = id === hoveredId
      marker.setStyle({ radius: active || hovered ? 7 : 5, fillOpacity: active ? 0.9 : hovered ? 0.75 : 0.5 })
    })
  }, [selectedId, hoveredId])

  const hoveredBuoy = buoys.find((b) => b.id === hoveredId)
  const selectedBuoy = buoys.find((b) => b.id === selectedId)

  return (
    <Modal
      title="Pick a NOAA buoy"
      subtitle={buoys.length > 0 ? `${buoys.length} NDBC buoys with a real historical wave record` : 'Loading buoy list… (first load can take up to a minute)'}
      width={900}
      onClose={onClose}
      footer={
        <>
          <div className="text-sm text-bm-navy">
            {hoveredBuoy ? (
              <span className="font-bold">{buoyLabel(hoveredBuoy)}</span>
            ) : selectedBuoy ? (
              <span className="font-bold">✓ {buoyLabel(selectedBuoy)}</span>
            ) : (
              <span className="text-bm-subtle">Click a buoy to select it — years shown are its actual historical coverage.</span>
            )}
          </div>
          <div className="flex gap-2">
            <Button variant="neutral" onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={() => selectedId && onConfirm(selectedId)} disabled={!selectedId}>
              Use this buoy
            </Button>
          </div>
        </>
      }
    >
      <div ref={mapDivRef} style={{ height: 460, width: '100%' }} />
    </Modal>
  )
}
