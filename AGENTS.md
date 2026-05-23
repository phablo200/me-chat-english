# Repository Guidelines

## Project Structure & Module Organization
This repository is a FastAPI backend.

- `main.py`: app entrypoint, middleware, CORS, and startup checks.
- `_core/`: shared infrastructure and configuration (`config.py`, `mongodb.py`, `llm_config.py`, middleware).
- `chat/`: chat domain (router, services, schemas, constants).
- `history/`: history domain (router, services, schemas, repository/db helpers).
- `docs/specs/` and `docs/plans/`: implementation specs and execution plans.

Keep new domain logic inside its module (`chat/`, `history/`) and place cross-cutting concerns in `_core/`.

## Build, Test, and Development Commands
- Install deps: `venv/bin/pip install -r requirements.txt`
- Run locally: `venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 3015`
- Quick syntax check: `python3 -m py_compile main.py _core/*.py chat/*.py history/*.py`

MongoDB is validated at startup; ensure `.env` contains valid `MONGODB_*` values before running.

## Coding Style & Naming Conventions
- Python 3.12, 4-space indentation, UTF-8.
- Use `snake_case` for modules/functions/variables; `PascalCase` for classes.
- Prefer explicit typing (as seen in `main.py` and `_core`).
- Keep routers thin; put business logic in `services.py` and persistence access in repository/db modules.
- Reuse `_core/config.py` for environment-driven settings.

## Testing Guidelines
There is no full test suite configured yet. For changes:

- Add focused unit tests when introducing logic-heavy functions.
- At minimum, run syntax checks and manually verify affected endpoints.
- For DB changes, validate startup behavior with correct and incorrect `MONGODB_*` env values.

Recommended future layout: `tests/<domain>/test_*.py`.

## Commit & Pull Request Guidelines
Use conventional-style, present-tense commit prefixes seen in history:

- `feat:` new behavior
- `fix:` bug fixes
- `config:` environment/tooling updates

Examples:
- `feat: add mongodb core configuration with startup validation`
- `fix: handle missing mongodb db name at startup`

PRs should include:
- clear scope and why the change is needed,
- linked spec/plan in `docs/` when relevant,
- local verification steps (commands run, endpoints tested).

## Security & Configuration Tips
- Never commit secrets; `.env` is ignored.
- Keep `.env.example` updated when adding new configuration keys.
- Pin dependency versions in `requirements.txt` to avoid runtime incompatibilities.
