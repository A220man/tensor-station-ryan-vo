# Changelog

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