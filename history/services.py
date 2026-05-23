from uuid import uuid4
from typing import Any

from history.constants import ALLOWED_MESSAGE_ROLES
from history.helper import parse_object_id
from history.repository import (
    create_conversation_doc,
    delete_conversation_by_id,
    get_conversation_by_id,
    push_message_to_conversation,
)


class InvalidMessageRoleError(ValueError):
    pass


class ConversationNotFoundError(ValueError):
    pass


def _validate_message_role(role: str) -> None:
    if role not in ALLOWED_MESSAGE_ROLES:
        raise InvalidMessageRoleError(
            f"Invalid message role. Allowed roles: {sorted(ALLOWED_MESSAGE_ROLES)}"
        )


async def start_conversation(
    *,
    user_id: str | None,
    title: str | None,
    role: str,
    content: str,
) -> dict[str, Any]:
    _validate_message_role(role)
    message_id = uuid4().hex
    conversation = await create_conversation_doc(
        user_id=user_id,
        title=title,
        role=role,
        content=content,
        message_id=message_id,
    )
    return {
        "conversation_id": str(conversation["_id"]),
        "message_id": message_id,
        "created_at": conversation["created_at"],
        "updated_at": conversation["updated_at"],
    }


async def append_message(
    *,
    conversation_id: str,
    role: str,
    content: str,
) -> dict[str, Any]:
    _validate_message_role(role)
    object_id = parse_object_id(conversation_id)
    existing = await get_conversation_by_id(object_id)
    if not existing:
        raise ConversationNotFoundError("Conversation not found.")

    message_id = uuid4().hex
    updated = await push_message_to_conversation(
        conversation_id=object_id,
        role=role,
        content=content,
        message_id=message_id,
    )
    if not updated:
        raise ConversationNotFoundError("Conversation not found.")

    refreshed = await get_conversation_by_id(object_id)
    if not refreshed:
        raise ConversationNotFoundError("Conversation not found.")

    return {
        "conversation_id": conversation_id,
        "message_id": message_id,
        "updated_at": refreshed["updated_at"],
    }


async def delete_conversation(*, conversation_id: str) -> dict[str, bool | str]:
    object_id = parse_object_id(conversation_id)
    deleted = await delete_conversation_by_id(object_id)
    if not deleted:
        raise ConversationNotFoundError("Conversation not found.")
    return {"conversation_id": conversation_id, "deleted": True}
