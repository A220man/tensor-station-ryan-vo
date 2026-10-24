/// <reference types="vitest/globals" />
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders header with title', () => {
    render(<App />)
    expect(screen.getByText('Tensor Station')).toBeInTheDocument()
  })

  it('renders execute button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: 'Execute' })).toBeInTheDocument()
  })

  it('renders node palette with items', () => {
    render(<App />)
    expect(screen.getByText('Checkpoint Loader')).toBeInTheDocument()
    expect(screen.getByText('KSampler')).toBeInTheDocument()
    expect(screen.getByText('VAE Decode')).toBeInTheDocument()
  })
})