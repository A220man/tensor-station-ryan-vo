import { useState, useCallback } from 'react'
import { Node, Edge, addEdge, Connection, ReactFlow, Background, Controls, MiniMap, useNodesState, useEdgesState, MarkerType } from 'reactflow'
import 'reactflow/dist/style.css'
import './App.css'

const initialNodes: Node[] = [
  { id: '1', type: 'input', position: { x: 250, y: 50 }, data: { label: 'Checkpoint Loader' } },
  { id: '2', position: { x: 250, y: 200 }, data: { label: 'CLIP Text Encode (Positive)' } },
  { id: '3', position: { x: 250, y: 350 }, data: { label: 'CLIP Text Encode (Negative)' } },
  { id: '4', position: { x: 500, y: 200 }, data: { label: 'KSampler' } },
  { id: '5', type: 'output', position: { x: 750, y: 200 }, data: { label: 'VAE Decode' } },
  { id: '6', position: { x: 1000, y: 200 }, data: { label: 'Save Image' } },
]

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e1-3', source: '1', target: '3', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2-4', source: '2', target: '4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3-4', source: '3', target: '4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e1-4', source: '1', target: '4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4-5', source: '4', target: '5', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e5-6', source: '5', target: '6', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
]

export default function App() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [selectedNode, setSelectedNode] = useState<Node | null>(null)

  const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges])

  const onNodeClick = useCallback((_evt: unknown, node: Node) => {
    setSelectedNode(node)
  }, [])

  return (
    <div className="app">
      <header className="header">
        <h1>Tensor Station</h1>
        <div className="header-actions">
          <button className="btn btn-primary" onClick={() => alert('Execute workflow (backend integration pending)')}>
            Execute
          </button>
          <button className="btn btn-secondary" onClick={() => alert('Save workflow (backend integration pending)')}>
            Save
          </button>
          <button className="btn btn-secondary" onClick={() => alert('Load workflow (backend integration pending)')}>
            Load
          </button>
        </div>
      </header>
      <div className="main-content">
        <aside className="sidebar">
          <h2>Nodes</h2>
          <div className="node-palette">
            <div className="palette-item" draggable={true} data-node-type="checkpoint_loader">
              Checkpoint Loader
            </div>
            <div className="palette-item" draggable={true} data-node-type="clip_encode">
              CLIP Text Encode
            </div>
            <div className="palette-item" draggable={true} data-node-type="ksampler">
              KSampler
            </div>
            <div className="palette-item" draggable={true} data-node-type="vae_decode">
              VAE Decode
            </div>
            <div className="palette-item" draggable={true} data-node-type="save_image">
              Save Image
            </div>
            <div className="palette-item" draggable={true} data-node-type="lora_loader">
              LoRA Loader
            </div>
            <div className="palette-item" draggable={true} data-node-type="controlnet">
              ControlNet
            </div>
          </div>
        </aside>
        <main className="canvas-wrapper">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            fitView
          >
            <Background />
            <Controls />
            <MiniMap />
          </ReactFlow>
        </main>
        {selectedNode && (
          <aside className="properties-panel">
            <h3>Node Properties</h3>
            <p>ID: {selectedNode.id}</p>
            <p>Type: {selectedNode.type || 'default'}</p>
            <pre>{JSON.stringify(selectedNode.data, null, 2)}</pre>
          </aside>
        )}
      </div>
    </div>
  )
}