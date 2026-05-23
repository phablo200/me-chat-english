# Create Initial MongoDB Configuration

## Objective
- Add an initial MongoDB configuration in `_core` that loads connection settings from new `.env` variables and makes those settings available for upcoming persistence features.

## Background
- The project already centralizes app-level environment configuration in [`_core/config.py`](/home/danii/myProjects/me-english-chat-backend/_core/config.py) using `python-dotenv` + `os.getenv`.
- There is currently no MongoDB configuration, no MongoDB dependency, and no shared database client/connection entrypoint.
- Existing modules (chat/history) are API/service oriented and can later consume a shared DB layer once configuration exists.

## Scope
### In Scope
- Define new MongoDB environment variables in `.env` (and document them in `.env.example` if introduced during implementation).
- Extend `_core/config.py` with MongoDB settings and safe defaults for local development.
- Add a new `_core` MongoDB module for creating/retrieving a Mongo client instance.
- Add dependency declarations required for MongoDB access.
- Ensure startup/runtime behavior is explicit when MongoDB variables are missing or malformed.

### Out of Scope
- Implementing chat/history repositories backed by MongoDB.
- Data migration from any existing storage.
- Production deployment infra changes (managed cluster provisioning, secrets manager wiring, network policy changes).

## Proposed Approach
- Keep configuration consistent with current patterns: load from `.env`, expose via `_core/config.py`, and keep `_core` as the shared infra boundary.
- Introduce the following environment variables:
  - `MONGODB_URI` (primary connection string)
  - `MONGODB_DB_NAME` (database name)
  - `MONGODB_CONNECT_TIMEOUT_MS` (optional timeout)
  - `MONGODB_SERVER_SELECTION_TIMEOUT_MS` (optional timeout)
- Update `Settings` in `_core/config.py` to expose typed Mongo settings.
- Add a new module (recommended: `_core/mongodb.py`) that:
  - Lazily builds a singleton Mongo client.
  - Exposes `get_mongodb_client()` and `get_database()` helpers.
  - Raises a clear error if required vars are absent.
- Add MongoDB driver dependency (recommended async-first: `motor`; alternative sync: `pymongo`).
- Integrate lightweight startup validation in app bootstrapping so misconfiguration fails fast in development.

Impacted areas/files:
- [`_core/config.py`](/home/danii/myProjects/me-english-chat-backend/_core/config.py)
- `_core/mongodb.py` (new)
- [`requirements.txt`](/home/danii/myProjects/me-english-chat-backend/requirements.txt)
- [`.env`](/home/danii/myProjects/me-english-chat-backend/.env)
- `.env.example` (new, recommended)
- [`main.py`](/home/danii/myProjects/me-english-chat-backend/main.py) (only if adding startup validation hook)

## Milestones
1. Configuration contract
- Add MongoDB env vars and defaults strategy.
- Extend `_core/config.py` with typed Mongo settings.

2. Mongo client bootstrap
- Add `_core/mongodb.py` with singleton client/database access helpers.
- Ensure clear exceptions/messages for invalid config.

3. Validation and readiness
- Add dependency to `requirements.txt`.
- Add startup or first-use validation path.
- Add/update docs for local setup.

## Edge Cases
- `MONGODB_URI` is missing while DB-dependent code path is called.
- `MONGODB_DB_NAME` is empty or whitespace.
- Timeout env vars are non-integer values.
- Local URI is reachable but authentication fails.
- App is started without MongoDB running in local environment.

## Acceptance Criteria
- [ ] `_core` contains a dedicated MongoDB configuration/connection module.
- [ ] MongoDB settings are loaded from `.env` through `_core/config.py`.
- [ ] Required Mongo variables are explicitly validated with actionable error messages.
- [ ] Project dependencies include the selected MongoDB driver.
- [ ] Local developer can configure and verify connection using documented env variables.

## Test Plan
- Unit:
  - Settings parsing for Mongo env vars (valid + invalid timeout values).
  - Client factory behavior when required vars are missing.

- Integration:
  - With a running local MongoDB instance, verify `get_database()` returns expected DB handle.
  - Validate startup/first-use failure path when URI is invalid.

- Manual verification:
  - Set `MONGODB_URI` and `MONGODB_DB_NAME` in `.env`.
  - Start app and confirm no configuration errors.
  - Temporarily break one required var and confirm clear failure message.

## Risks and Mitigations
- Risk: Secrets leakage by committing real Mongo credentials in `.env`.
  - Mitigation: Keep `.env` ignored, add `.env.example` placeholders, and avoid real secrets in tracked files.

- Risk: Sync/async driver mismatch with FastAPI usage patterns.
  - Mitigation: Prefer `motor` to align with async stack and avoid blocking event loop.

- Risk: Implicit connection attempts can slow startup.
  - Mitigation: Use lazy initialization and bounded server-selection timeout.

## Open Questions
- Should MongoDB be mandatory at app startup, or optional until a DB-backed endpoint is called? Mandatory at startup.
- Do we want one shared database (`MONGODB_DB_NAME`) for all modules, or per-domain DB names/collections in config? One for all modules.
- Should we standardize on `motor` now, or keep abstraction flexible for `pymongo` fallback? we can standardize.
