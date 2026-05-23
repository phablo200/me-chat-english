# History Conversation Lifecycle (Start, Continue, Delete)

## Objective
- Implement initial history capabilities so a user can:
  - start a new conversation,
  - continue an existing conversation,
  - delete a conversation.
- Define required MongoDB data models in `history/db.py` and place each method in the correct `history` layer file.

## Background / Current Behavior
- MongoDB bootstrap exists in `_core/mongodb.py` (`get_database()` and startup ping).
- `history/` structure exists but files are empty (`router.py`, `services.py`, `repository.py`, `db.py`, `schemas.py`, `helper.py`, `constants.py`).
- No endpoints, schemas, persistence model, or service orchestration currently exist for conversation history.

## Scope
### In Scope
- Add conversation lifecycle API contracts (start/continue/delete) in `history/router.py`.
- Add request/response schemas in `history/schemas.py`.
- Add domain service orchestration in `history/services.py`.
- Add persistence methods in `history/repository.py`.
- Add MongoDB model/collection contracts in `history/db.py`.
- Add shared constants and small utility helpers where needed.

### Out of Scope
- Authentication/authorization rules.
- Full-text search, pagination, or analytics.
- Soft-delete/restore (hard delete only for initial scope).

## Proposed Approach
- Use one collection `conversations` with embedded messages for initial simplicity.
- `history/db.py` will define model contract:
  - `ConversationDocument`: `_id`, `user_id`, `title`, `created_at`, `updated_at`, `messages[]`, `status`.
  - `MessageDocument`: `message_id`, `role`, `content`, `created_at`.
- Method ownership by file:
  - `history/router.py`:
    - `POST /history/conversations` -> start conversation
    - `POST /history/conversations/{conversation_id}/messages` -> continue conversation
    - `DELETE /history/conversations/{conversation_id}` -> delete conversation
  - `history/services.py`:
    - `start_conversation(...)`
    - `append_message(...)`
    - `delete_conversation(...)`
  - `history/repository.py`:
    - `create_conversation_doc(...)`
    - `push_message_to_conversation(...)`
    - `get_conversation_by_id(...)`
    - `delete_conversation_by_id(...)`
  - `history/helper.py`:
    - `utcnow()` and ID conversion/validation helpers.
  - `history/constants.py`:
    - collection name and allowed message roles.

## Milestones / Implementation Plan
1. API and schema contract
- Define Pydantic request/response models in `history/schemas.py`.
- Register router and endpoint signatures in `history/router.py`.

2. Data model and repository
- Define document shapes and collection access in `history/db.py`.
- Implement CRUD primitives in `history/repository.py` using `_core.mongodb.get_database()`.

3. Services and endpoint wiring
- Implement lifecycle business logic in `history/services.py`.
- Wire routes to services and map repository/service errors to HTTP exceptions.

4. App integration
- Include history router from `main.py`.
- Verify startup and route availability.

## Acceptance Criteria
- [ ] User can create a conversation and receive `conversation_id`.
- [ ] User can append a message to an existing conversation.
- [ ] User gets a clear `404` when continuing/deleting a missing conversation.
- [ ] User can delete an existing conversation and receive success response.
- [ ] MongoDB models are defined in `history/db.py` and used by repository/service layers.
- [ ] Methods are placed in their intended architectural files (`router/services/repository/db`).

## Test Plan
- Unit:
  - Service behavior for start/append/delete with mocked repository.
  - Helper validation for malformed `conversation_id`.
- Integration:
  - Create -> append -> delete flow against local MongoDB.
  - Continue/delete on unknown ID returns expected HTTP status.
- Manual:
  - Call three endpoints with `curl`/Postman and verify persisted data in `conversations` collection.

## Risks and Mitigations
- Risk: Embedded messages grow large for long conversations.
  - Mitigation: Accept for initial version; future split into `messages` collection when limits are approached.
- Risk: Invalid ObjectId inputs causing server errors.
  - Mitigation: Centralize ID validation in `helper.py` and return controlled client errors.
- Risk: Inconsistent timestamps and ordering.
  - Mitigation: Use single UTC helper and update `updated_at` on each append.

## Open Questions
- Should `user_id` be required at this stage, or optional until auth is integrated? optional until auth is integrated.
- Should delete be hard delete (initial recommendation) or soft delete via `status` flag? hard delete.
- Should start conversation require an initial message, or allow empty conversation creation? require a initial message.
