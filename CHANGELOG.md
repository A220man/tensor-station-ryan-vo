# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint

### Added
- Inference request validation with optional `model_id` field referencing registered models
- Model validation dependency returning 404 for unregistered model IDs
- Enhanced inference simulation with progress tracking (0.0–1.0), step counting, and error handling
- Batch size support generating multiple result URLs per execution
- Improved cancel endpoint for queued/running executions
- New inference tests covering model validation, batch inference, and error cases

### Verified
- All backend tests pass (16/16)
- All frontend tests pass (3/3)
- Manual API testing confirms model validation, progress tracking, batch results, and cancellation

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — work-in-progress checkpoint

### Fixed
- datetime.utcnow() deprecation warnings replaced with timezone-aware datetime.now(UTC) across all API modules
- Pydantic class-based Config migrated to ConfigDict in WorkflowResponse, ModelInfo, ModelLoadRequest, ModelLoadResponse
- Pydantic protected_namespaces warnings resolved for model_id fields

### Verified
- All backend tests pass (14/14)
- All frontend tests pass (3/3)
- Frontend TypeScript compilation and Vite build successful
- FastAPI app starts and serves health endpoint

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-10-20

### Added
- Initial project skeleton with FastAPI backend and React frontend
- Health check endpoint
- Workflow CRUD API (create, read, update, delete, list)
- Model registration and loading API
- Inference queue and execution status API
- ReactFlow-based visual workflow editor
- Node palette with diffusion node types
- Properties panel for node inspection
- Docker Compose with PostgreSQL, Keycloak, backend, frontend
- Backend tests (health, workflows, models, inference)
- Frontend tests (App component)
- CI/CD pipeline configuration
- Portfolio.json with project metadata

### Security
- OIDC authentication configured for Keycloak integration
- Environment-based secrets management
- Non-root Docker users
