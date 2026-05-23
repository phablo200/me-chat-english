import os
from dotenv import load_dotenv

load_dotenv()


def _parse_int_env(var_name: str, default: str) -> int:
    raw_value = os.getenv(var_name, default)
    try:
        return int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{var_name} must be an integer, got '{raw_value}'") from exc


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "").strip()
    MONGODB_CONNECT_TIMEOUT_MS: int = _parse_int_env(
        "MONGODB_CONNECT_TIMEOUT_MS", "3000"
    )
    MONGODB_SERVER_SELECTION_TIMEOUT_MS: int = _parse_int_env(
        "MONGODB_SERVER_SELECTION_TIMEOUT_MS", "3000"
    )

settings = Settings()
