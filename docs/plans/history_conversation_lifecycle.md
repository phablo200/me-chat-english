# Plan: History Conversation Lifecycle

## Goal
Implement initial history lifecycle support so users can start a conversation, continue an existing conversation, and delete a conversation.

## Inputs
- Spec: [`docs/specs/history_conversation_lifecycle.md`](/home/danii/myProjects/me-english-chat-backend/docs/specs/history_conversation_lifecycle.md)
- Architectural decisions from spec:
  - Use one `conversations` collection with embedded `messages`.
  - Hard delete for this initial version.
  - `user_id` optional until auth is integrated.
  - Start conversation requires an initial message.

## Constraints
- Keep method ownership aligned to the existing domain layers:
  - routing in `history/router.py`
  - orchestration in `history/services.py`
  - persistence in `history/repository.py`
  - document model/contracts in `history/db.py`
- Reuse `_core/mongodb.py` (`get_database`) instead of introducing new DB bootstrap paths.
- Keep scope limited to lifecycle endpoints (no search, pagination, restore flows, or auth rules).

## Deliverables
- Completed lifecycle API routes in [`history/router.py`](/home/danii/myProjects/me-english-chat-backend/history/router.py):
  - `POST /history/conversations`
  - `POST /history/conversations/{conversation_id}/messages`
  - `DELETE /history/conversations/{conversation_id}`
- Request/response schemas in [`history/schemas.py`](/home/danii/myProjects/me-english-chat-backend/history/schemas.py).
- Mongo model contract definitions and collection access patterns in [`history/db.py`](/home/danii/myProjects/me-english-chat-backend/history/db.py).
- CRUD repository methods in [`history/repository.py`](/home/danii/myProjects/me-english-chat-backend/history/repository.py).
- Lifecycle service methods in [`history/services.py`](/home/danii/myProjects/me-english-chat-backend/history/services.py).
- Supporting constants/helpers in [`history/constants.py`](/home/danii/myProjects/me-english-chat-backend/history/constants.py) and [`history/helper.py`](/home/danii/myProjects/me-english-chat-backend/history/helper.py).
- Router inclusion from [`main.py`](/home/danii/myProjects/me-english-chat-backend/main.py).

## Implementation Plan
1. Define API and schema contract
- Add request/response Pydantic models for start/append/delete flows.
- Define endpoint signatures and response codes in the history router.
- Standardize error payload shape for invalid IDs and missing conversations.

2. Define DB document contracts
- Add typed document shapes for conversation and message records in `history/db.py`.
- Centralize collection naming and role constraints.
- Ensure timestamps are consistently UTC and persisted on create/update.

3. Implement repository primitives
- Implement `create_conversation_doc(...)`.
- Implement `get_conversation_by_id(...)`.
- Implement `push_message_to_conversation(...)`.
- Implement `delete_conversation_by_id(...)`.
- Handle ObjectId conversion and not-found outcomes deterministically.

4. Implement service orchestration
- Implement `start_conversation(...)` with required initial message validation.
- Implement `append_message(...)` with conversation existence checks.
- Implement `delete_conversation(...)` mapping not-found to domain-level errors.
- Keep HTTP concerns out of service layer; return domain results/errors.

5. Wire routes and app integration
- Connect router handlers to service methods.
- Translate domain/repository errors to HTTP status codes (notably `404`).
- Register history router in `main.py` and verify route exposure.

## Execution Order
1. Schemas + constants/helpers
2. DB contracts (`history/db.py`)
3. Repository methods
4. Service methods
5. Router wiring + `main.py` integration
6. Verification

## Verification Plan
- Syntax checks:
  - `python3 -m py_compile main.py _core/*.py chat/*.py history/*.py`

- Functional checks (manual/API):
  - Start conversation returns a new `conversation_id`.
  - Append message to existing conversation succeeds and updates `updated_at`.
  - Append/delete with unknown `conversation_id` returns `404`.
  - Delete existing conversation returns success and document is removed.

- Data checks (Mongo):
  - `conversations` documents include required fields (`_id`, `title`, timestamps, `messages`, status).
  - Message entries include required fields (`message_id`, `role`, `content`, `created_at`).
  - Timestamp ordering is consistent across create and append operations.

## Risks and Mitigations
- Risk: Embedded message arrays can grow toward MongoDB document limits.
- Mitigation: Accept for MVP and document migration path to split `messages` collection.

- Risk: Invalid `conversation_id` values trigger unhandled conversion errors.
- Mitigation: Centralize ID validation/conversion helpers and map failures to client-safe errors.

- Risk: Layer leakage (router logic in services/repository or vice versa).
- Mitigation: Keep strict function boundaries and review method placement during implementation.

## Non-Goals
- Authentication/authorization behavior.
- Soft delete, archive, or restore lifecycle.
- Search/list/history pagination endpoints.
- Index tuning and performance optimization beyond baseline correctness.
