# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

project-skeleton

## Roadmap

### project-skeleton — Project Skeleton with FastAPI Backend and React Frontend

Status: in_progress

Acceptance:
- FastAPI app starts and serves health endpoint
- React + TypeScript + Vite frontend builds
- Docker compose brings up backend, frontend, Keycloak, PostgreSQL
- Backend tests pass (pytest)
- Frontend typecheck and build pass
- portfolio.json created with required fields

Implementation: `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/api/health.py`, `backend/requirements.txt`, `backend/tests/test_health.py`, `frontend/package.json`, `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/api/client.ts`, `docker-compose.yaml`, `backend/Dockerfile`, `frontend/Dockerfile`, `portfolio.json`

Tests: `backend/tests/test_health.py`, `frontend/src/App.test.tsx`

### workflow-graph-editor — Node-based Workflow Graph Editor

Status: planned

Acceptance:
- Canvas with pan/zoom
- Add/remove nodes
- Connect nodes with edges
- Save/load workflow JSON
- Execute workflow via backend API

### model-management — Model Loading and Caching

Status: planned

Acceptance:
- Load diffusion models from disk
- Cache models in VRAM/RAM
- Hot-swap models without reload
- Memory pressure handling

### inference-engine — Fast Local Inference Engine

Status: planned

Acceptance:
- Run diffusion sampling
- Support multiple schedulers
- Progress callbacks
- Cancel/queue management

### auth-oidc — OIDC Authentication with Keycloak

Status: planned

Acceptance:
- Login/logout flow
- Role-based access (viewer/operator/admin)
- Protected API endpoints
- Session management

### llm-adapters — LLM Provider Adapters

Status: planned

Acceptance:
- OpenAI-compatible adapter
- Anthropic adapter
- Gemini adapter
- Ollama adapter
- Configurable via env vars

