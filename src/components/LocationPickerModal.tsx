import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { Button, Modal } from './ui'

// Vite bundles Leaflet's default marker images under hashed URLs, which breaks Leaflet's own
// (webpack-era) lookup logic -- point it at the bundled assets explicitly.
delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

// Generic "click anywhere on the map" lat/long picker -- today only used for Copernicus
// Marine (StudyBuilder.tsx), since Copernicus is a global reanalysis grid where any
// coordinate is valid. NDBC deliberately does NOT use this: it has its own
// NdbcBuoyPickerModal that only offers real buoy locations, since resolving an arbitrary
// lat/long to "whichever buoy happens to be nearest" can silently pick one hundreds of km
// away (see that component + pybm_service.py's ndbc branch for the full story).
interface Props {
  initialLat?: number | null
  initialLng?: number | null
  onConfirm: (lat: number, lng: number) => void
  onClose: () => void
}

export default function LocationPickerModal({ initialLat, initialLng, onConfirm, onClose }: Props) {
  const mapDivRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const markerRef = useRef<L.Marker | null>(null)
  const [picked, setPicked] = useState<{ lat: number; lng: number } | null>(
    initialLat != null && initialLng != null ? { lat: initialLat, lng: initialLng } : null
  )

  // Mount-once: initialLat/initialLng only set the starting view and marker. StudyBuilder
  // mounts this modal fresh each time it opens, so they never change while it's open.
  useEffect(() => {
    if (!mapDivRef.current || mapRef.current) return
    // Defaults to roughly the North Sea if nothing was picked yet, zoomed further out
    // (3 vs 5) so "nothing picked" doesn't look like it's already centered on a specific spot.
    const startLat = initialLat ?? 54
    const startLng = initialLng ?? 3
    const map = L.map(mapDivRef.current).setView([startLat, startLng], initialLat != null ? 5 : 3)
    mapRef.current = map

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 12,
    }).addTo(map)

    if (initialLat != null && initialLng != null) {
      markerRef.current = L.marker([initialLat, initialLng]).addTo(map)
    }

    // Every click moves (or creates) the single marker and updates `picked`, which is
    // what the footer's coordinate readout and "Use this location" button read from.
    map.on('click', (e: L.LeafletMouseEvent) => {
      const { lat, lng } = e.latlng
      setPicked({ lat, lng })
      if (markerRef.current) {
        markerRef.current.setLatLng(e.latlng)
      } else {
        markerRef.current = L.marker(e.latlng).addTo(map)
      }
    })

    // The map div isn't visible-sized until the modal has painted -- recalc once it has.
    setTimeout(() => map.invalidateSize(), 50)

    return () => {
      map.remove()
      mapRef.current = null
      markerRef.current = null
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <Modal
      title="Pick a location"
      width={720}
      onClose={onClose}
      footer={
        <>
          <div className="text-sm text-bm-navy">
            {picked ? (
              <span className="font-bold">
                {picked.lat.toFixed(4)}, {picked.lng.toFixed(4)}
              </span>
            ) : (
              <span className="text-bm-subtle">Click the map to choose a point</span>
            )}
          </div>
          <div className="flex gap-2">
            <Button variant="neutral" onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={() => picked && onConfirm(picked.lat, picked.lng)} disabled={!picked}>
              Use this location
            </Button>
          </div>
        </>
      }
    >
      <div ref={mapDivRef} style={{ height: 420, width: '100%' }} />
    </Modal>
  )
}
