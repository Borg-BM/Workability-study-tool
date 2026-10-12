// The shared backdrop behind every popup (ui.tsx's Modal): dims the page slightly, locks the
// page's own scrolling while open (so the mouse wheel never scrolls the page behind the popup),
// and closes the popup on a click outside it or on Escape. A popup taller than the window
// scrolls inside the backdrop instead of running off the screen.
import { useEffect, useRef, type ReactNode } from 'react'

export default function ModalBackdrop({ onClose, children }: { onClose: () => void; children: ReactNode }) {
  const closeRef = useRef(onClose)
  closeRef.current = onClose
  // Only a click that also started outside the popup closes it -- selecting text in an
  // input and releasing the mouse over the backdrop shouldn't throw the popup away.
  const pressedOutside = useRef(false)

  useEffect(() => {
    const { style } = document.body
    const previous = { overflow: style.overflow, paddingRight: style.paddingRight }
    // Hiding the page scrollbar would otherwise shift the page sideways behind the popup.
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth
    style.overflow = 'hidden'
    if (scrollbarWidth > 0) style.paddingRight = `${scrollbarWidth}px`
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeRef.current()
    }
    window.addEventListener('keydown', onKeyDown)
    return () => {
      style.overflow = previous.overflow
      style.paddingRight = previous.paddingRight
      window.removeEventListener('keydown', onKeyDown)
    }
  }, [])

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" style={{ background: 'rgba(5,22,66,0.3)' }}>
      <div
        className="min-h-full flex items-center justify-center p-4"
        onMouseDown={(e) => {
          pressedOutside.current = e.target === e.currentTarget
        }}
        onClick={(e) => {
          if (pressedOutside.current && e.target === e.currentTarget) closeRef.current()
        }}
      >
        {children}
      </div>
    </div>
  )
}
