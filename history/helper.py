from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError) as exc:
        raise ValueError("Invalid conversation_id format.") from exc
