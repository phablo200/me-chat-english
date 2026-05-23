from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from _core.config import settings

_mongo_client: AsyncIOMotorClient | None = None


def validate_mongodb_settings() -> None:
    if not settings.MONGODB_URI.strip():
        raise ValueError(
            "Missing required env var MONGODB_URI. Set it in .env before starting the app."
        )
    if not settings.MONGODB_DB_NAME:
        raise ValueError(
            "Missing required env var MONGODB_DB_NAME. Set it in .env before starting the app."
        )


def get_mongodb_client() -> AsyncIOMotorClient:
    global _mongo_client
    validate_mongodb_settings()

    if _mongo_client is None:
        _mongo_client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            connectTimeoutMS=settings.MONGODB_CONNECT_TIMEOUT_MS,
            serverSelectionTimeoutMS=settings.MONGODB_SERVER_SELECTION_TIMEOUT_MS,
        )
    return _mongo_client


def get_database() -> AsyncIOMotorDatabase:
    return get_mongodb_client()[settings.MONGODB_DB_NAME]


async def validate_mongodb_connection() -> None:
    client = get_mongodb_client()
    await client.admin.command("ping")
