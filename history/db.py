from typing import Any, TypedDict

from motor.motor_asyncio import AsyncIOMotorCollection

from _core.mongodb import get_database
from history.constants import CONVERSATION_STATUS_ACTIVE, CONVERSATIONS_COLLECTION
from history.helper import utcnow


class MessageDocument(TypedDict):
    message_id: str
    role: str
    content: str
    created_at: Any


class ConversationDocument(TypedDict):
    user_id: str | None
    title: str | None
    created_at: Any
    updated_at: Any
    messages: list[MessageDocument]
    status: str


def get_conversations_collection() -> AsyncIOMotorCollection[dict[str, Any]]:
    db = get_database()
    return db[CONVERSATIONS_COLLECTION]


def build_message_document(*, message_id: str, role: str, content: str) -> MessageDocument:
    return {
        "message_id": message_id,
        "role": role,
        "content": content,
        "created_at": utcnow(),
    }


def build_conversation_document(
    *,
    user_id: str | None,
    title: str | None,
    initial_message: MessageDocument,
) -> ConversationDocument:
    now = utcnow()
    return {
        "user_id": user_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": [initial_message],
        "status": CONVERSATION_STATUS_ACTIVE,
    }
