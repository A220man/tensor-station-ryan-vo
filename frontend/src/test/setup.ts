import { vi } from 'vitest'
import React, { ReactNode } from 'react'

// Mock reactflow
vi.mock('reactflow', () => ({
  Node: ({ children }: { children: ReactNode }) => React.createElement('div', { 'data-testid': 'node' }, children),
  Edge: () => React.createElement('div', { 'data-testid': 'edge' }),
  ReactFlow: ({ children }: { children: ReactNode }) => React.createElement('div', { 'data-testid': 'react-flow' }, children),
  Background: () => React.createElement('div', { 'data-testid': 'background' }),
  Controls: () => React.createElement('div', { 'data-testid': 'controls' }),
  MiniMap: () => React.createElement('div', { 'data-testid': 'minimap' }),
  useNodesState: (initial: unknown) => [initial, vi.fn(), vi.fn()],
  useEdgesState: (initial: unknown) => [initial, vi.fn(), vi.fn()],
  addEdge: (params: unknown, edges: unknown[]) => [...edges, { id: 'new', ...(params as object) }],
  MarkerType: { ArrowClosed: 'arrowclosed' },
  Connection: {},
}))