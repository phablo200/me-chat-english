from typing import Any

from bson import ObjectId

from history.db import (
    build_conversation_document,
    build_message_document,
    get_conversations_collection,
)
from history.helper import utcnow


async def create_conversation_doc(
    *,
    user_id: str | None,
    title: str | None,
    role: str,
    content: str,
    message_id: str,
) -> dict[str, Any]:
    collection = get_conversations_collection()
    initial_message = build_message_document(
        message_id=message_id,
        role=role,
        content=content,
    )
    conversation_doc = build_conversation_document(
        user_id=user_id,
        title=title,
        initial_message=initial_message,
    )
    result = await collection.insert_one(conversation_doc)
    conversation_doc["_id"] = result.inserted_id
    return conversation_doc


async def get_conversation_by_id(conversation_id: ObjectId) -> dict[str, Any] | None:
    collection = get_conversations_collection()
    return await collection.find_one({"_id": conversation_id})


async def push_message_to_conversation(
    *,
    conversation_id: ObjectId,
    role: str,
    content: str,
    message_id: str,
) -> bool:
    collection = get_conversations_collection()
    message_doc = build_message_document(
        message_id=message_id,
        role=role,
        content=content,
    )
    result = await collection.update_one(
        {"_id": conversation_id},
        {
            "$push": {"messages": message_doc},
            "$set": {"updated_at": utcnow()},
        },
    )
    return result.matched_count == 1


async def delete_conversation_by_id(conversation_id: ObjectId) -> bool:
    collection = get_conversations_collection()
    result = await collection.delete_one({"_id": conversation_id})
    return result.deleted_count == 1
