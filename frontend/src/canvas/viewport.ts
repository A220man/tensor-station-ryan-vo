// Pure viewport helpers for the workflow canvas pan/zoom behavior.
// Kept free of React/ReactFlow so the math is unit-testable in isolation.

export interface Viewport {
  x: number
  y: number
  zoom: number
}

export const MIN_ZOOM = 0.25
export const MAX_ZOOM = 2.5

/** Clamp a zoom value into the supported [MIN_ZOOM, MAX_ZOOM] range. */
export function clampZoom(zoom: number): number {
  if (Number.isNaN(zoom)) return MIN_ZOOM
  return Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, zoom))
}

/**
 * Clamp a viewport so its zoom stays in range and its pan offset stays within
 * `bounds` (in screen pixels). Non-finite input falls back to a safe default.
 */
export function clampViewport(viewport: Viewport, bounds: { width: number; height: number }): Viewport {
  const zoom = clampZoom(viewport.zoom)
  const x = Number.isFinite(viewport.x) ? viewport.x : 0
  const y = Number.isFinite(viewport.y) ? viewport.y : 0
  const width = Number.isFinite(bounds.width) && bounds.width > 0 ? bounds.width : 0
  const height = Number.isFinite(bounds.height) && bounds.height > 0 ? bounds.height : 0
  return {
    zoom,
    x: Math.min(width, Math.max(-width, x)),
    y: Math.min(height, Math.max(-height, y)),
  }
}
