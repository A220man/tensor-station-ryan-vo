/// <reference types="vitest/globals" />
import { clampZoom, clampViewport, MIN_ZOOM, MAX_ZOOM } from './viewport'

describe('clampZoom', () => {
  it('keeps in-range zoom unchanged', () => {
    expect(clampZoom(1)).toBe(1)
    expect(clampZoom(MIN_ZOOM)).toBe(MIN_ZOOM)
    expect(clampZoom(MAX_ZOOM)).toBe(MAX_ZOOM)
  })

  it('clamps zoom below the minimum up to MIN_ZOOM', () => {
    expect(clampZoom(0.1)).toBe(MIN_ZOOM)
    expect(clampZoom(-5)).toBe(MIN_ZOOM)
  })

  it('clamps zoom above the maximum down to MAX_ZOOM', () => {
    expect(clampZoom(9)).toBe(MAX_ZOOM)
  })

  it('falls back to MIN_ZOOM for NaN', () => {
    expect(clampZoom(NaN)).toBe(MIN_ZOOM)
  })
})

describe('clampViewport', () => {
  const bounds = { width: 1000, height: 800 }

  it('leaves a valid viewport unchanged', () => {
    const vp = { x: 100, y: -50, zoom: 1.2 }
    expect(clampViewport(vp, bounds)).toEqual(vp)
  })

  it('clamps zoom while preserving finite pan', () => {
    const out = clampViewport({ x: 10, y: 20, zoom: 99 }, bounds)
    expect(out.zoom).toBe(MAX_ZOOM)
    expect(out.x).toBe(10)
    expect(out.y).toBe(20)
  })

  it('clamps pan offsets to +/- bounds', () => {
    const out = clampViewport({ x: 5000, y: -5000, zoom: 1 }, bounds)
    expect(out.x).toBe(1000)
    expect(out.y).toBe(-800)
  })

  it('falls back to safe defaults for non-finite input', () => {
    const out = clampViewport({ x: NaN, y: Infinity, zoom: NaN }, bounds)
    expect(out).toEqual({ x: 0, y: 0, zoom: MIN_ZOOM })
  })
})
