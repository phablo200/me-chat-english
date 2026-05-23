# Plan: Create Initial MongoDB Configuration

## Goal
Implement initial MongoDB configuration support in `_core` using `.env` variables, without adding feature-level persistence yet.

## Inputs
- Spec: [`docs/specs/create_initial_mongodb_conf.md`](/home/danii/myProjects/me-english-chat-backend/docs/specs/create_initial_mongodb_conf.md)
- Architectural decision from spec:
  - MongoDB is mandatory at startup.
  - One shared database name for all modules.
  - Standardize on `motor`.

## Constraints
- Keep the existing configuration style (`python-dotenv` + `os.getenv`) centered in `_core/config.py`.
- No repository/service migrations for `chat` or `history` in this scope.
- Do not store real credentials in tracked files.

## Deliverables
- Updated [`_core/config.py`](/home/danii/myProjects/me-english-chat-backend/_core/config.py) with typed MongoDB settings.
- New `_core/mongodb.py` module with singleton async client/database access helpers.
- Updated [`requirements.txt`](/home/danii/myProjects/me-english-chat-backend/requirements.txt) with `motor`.
- Updated [`.env`](/home/danii/myProjects/me-english-chat-backend/.env) with MongoDB vars (local/dev values).
- New `.env.example` containing placeholder MongoDB vars and non-secret defaults.
- Optional startup validation in [`main.py`](/home/danii/myProjects/me-english-chat-backend/main.py) to fail fast when config is invalid.

## Implementation Plan
1. Define env contract
- Add `MONGODB_URI` (required), `MONGODB_DB_NAME` (required), `MONGODB_CONNECT_TIMEOUT_MS` (optional), and `MONGODB_SERVER_SELECTION_TIMEOUT_MS` (optional).
- Set development-safe default values only for optional timeout fields.
- Add equivalent placeholder keys in `.env.example`.

2. Extend centralized settings
- Add MongoDB fields to `Settings` in `_core/config.py` with explicit type conversion.
- Ensure invalid integer conversion for timeout fields raises a clear error message.
- Normalize or validate `MONGODB_DB_NAME` to reject empty/whitespace-only values.

3. Add MongoDB bootstrap module
- Create `_core/mongodb.py` with:
  - Lazy singleton `AsyncIOMotorClient` construction.
  - `get_mongodb_client()` returning singleton client.
  - `get_database()` returning `client[settings.MONGODB_DB_NAME]`.
- Add config validation helper(s) that check required fields and emit actionable errors.

4. Add startup validation path
- In `main.py`, add a startup event/lifespan hook that validates MongoDB configuration at app boot.
- Keep connection validation bounded by configured timeouts to avoid long boot hangs.

5. Dependency and docs updates
- Add `motor` to `requirements.txt`.
- Document local setup expectations (MongoDB required at startup; env variables to set).

## Execution Order
1. Env + config contract
2. Mongo module
3. Startup validation hook
4. Dependency + env example/docs
5. Verification

## Verification Plan
- Static checks:
  - App imports succeed after adding `motor` and new `_core/mongodb.py`.
  - No circular imports introduced between `_core/config.py`, `_core/mongodb.py`, and `main.py`.

- Functional checks:
  - App starts successfully when required Mongo vars are valid.
  - App fails fast at startup with clear message when `MONGODB_URI` or `MONGODB_DB_NAME` is missing/invalid.
  - Timeout vars accept integer strings and fail clearly on non-integer values.

- Manual checks:
  - Start app with local Mongo instance and confirm healthy startup.
  - Break one required variable and confirm deterministic startup error.

## Risks and Mitigations
- Risk: Secrets accidentally committed.
- Mitigation: Keep real secrets in `.env` only and use placeholder values in `.env.example`.

- Risk: Startup instability if Mongo is unreachable.
- Mitigation: Use strict but bounded timeout configuration and explicit failure messages.

- Risk: Async misuse in future repository code.
- Mitigation: Standardize now on `motor` and expose one shared async access module.

## Non-Goals
- Implementing Mongo-backed chat/history repositories.
- Collection schema design and index provisioning.
- Production secrets/distributed configuration management.
