import { useEffect, useMemo, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { ApiLocation } from '../api'
import { Button, Modal } from './ui'

// Map picker for one of the 104 DNV-RP-C205 nautic zones -- each zone is drawn as a
// rectangle from its bbox (see weibull_locations.py's _ZONE_BBOX for where the
// boundaries come from). `locations` is normally loaded before this opens, but rectangle
// drawing is its own effect keyed on it (not just mount), so a list that arrives after the
// modal opened still gets drawn -- same as NdbcBuoyPickerModal.
interface Props {
  locations: ApiLocation[]
  initialLocationId?: string | null
  onConfirm: (locationId: string) => void
  onClose: () => void
}

export default function WeibullZonePickerModal({ locations, initialLocationId, onConfirm, onClose }: Props) {
  const mapDivRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const rectRef = useRef<Map<string, L.Rectangle>>(new Map())
  const [hoveredId, setHoveredId] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(initialLocationId ?? null)

  // Every ApiLocation has a bbox in practice (all 104 built-in zones do) -- filtered
  // defensively anyway in case that ever changes. Memoized so the rectangle-drawing effect
  // below (keyed on this array) only re-runs when `locations` itself actually changes, not
  // on every hover/select re-render (a plain .filter() with no memoization would produce a
  // new array -- and thus a new effect run -- on every render, tearing down and rebuilding
  // all 104 rectangles constantly).
  const zoneLocations = useMemo(() => locations.filter((l) => l.bbox), [locations])

  useEffect(() => {
    if (!mapDivRef.current || mapRef.current) return
    const map = L.map(mapDivRef.current, { worldCopyJump: false }).setView([20, 10], 2)
    mapRef.current = map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 8,
      minZoom: 2,
    }).addTo(map)

    setTimeout(() => map.invalidateSize(), 50)

    return () => {
      map.remove()
      mapRef.current = null
      rectRef.current.clear()
    }
  }, [])

  // Separate from map init (see the file-level comment above).
  useEffect(() => {
    const map = mapRef.current
    if (!map) return

    rectRef.current.forEach((rect) => map.removeLayer(rect))
    rectRef.current.clear()

    zoneLocations.forEach((loc) => {
      const b = loc.bbox!
      const rect = L.rectangle(
        [
          [b.lat_min, b.lon_min],
          [b.lat_max, b.lon_max],
        ],
        {
          color: '#00ADEF',
          weight: 1,
          fillColor: '#00ADEF',
          fillOpacity: loc.id === selectedId ? 0.55 : 0.12,
        }
      ).addTo(map)

      rect.on('mouseover', () => setHoveredId(loc.id))
      rect.on('mouseout', () => setHoveredId((h) => (h === loc.id ? null : h)))
      rect.on('click', () => setSelectedId(loc.id))
      rect.bindTooltip(loc.label, { sticky: true })

      rectRef.current.set(loc.id, rect)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [zoneLocations])

  // Keeps fill opacity in sync with hover/select state without redrawing every rectangle.
  useEffect(() => {
    rectRef.current.forEach((rect, id) => {
      rect.setStyle({ fillOpacity: id === selectedId ? 0.55 : id === hoveredId ? 0.4 : 0.12 })
    })
  }, [selectedId, hoveredId])

  const hoveredLocation = locations.find((l) => l.id === hoveredId)
  const selectedLocation = locations.find((l) => l.id === selectedId)

  return (
    <Modal
      title="Pick a DNV nautic zone"
      subtitle="DNV-RP-C205 Appendix B/C — 104 zones"
      width={860}
      onClose={onClose}
      footer={
        <>
          <div className="text-sm text-bm-navy">
            {hoveredLocation ? (
              <span className="font-bold">{hoveredLocation.label}</span>
            ) : selectedLocation ? (
              <span className="font-bold">✓ {selectedLocation.label}</span>
            ) : (
              <span className="text-bm-subtle">Click a zone to select it</span>
            )}
          </div>
          <div className="flex gap-2">
            <Button variant="neutral" onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={() => selectedId && onConfirm(selectedId)} disabled={!selectedId}>
              Use this zone
            </Button>
          </div>
        </>
      }
    >
      <div ref={mapDivRef} style={{ height: 440, width: '100%' }} />
    </Modal>
  )
}
