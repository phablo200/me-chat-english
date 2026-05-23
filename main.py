import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from _core.mongodb import validate_mongodb_connection
from history.router import router as history_router

app = FastAPI(title="MeEnglishChat")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

FRONTEND_ORIGINS = [
    "http://localhost:4004",
    "http://127.0.0.1:4004",
    "http://localhost:4009",
    "http://localhost:4010",
    "http://127.0.0.1:4009",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(history_router)


@app.on_event("startup")
async def startup_check_mongodb() -> None:
    await validate_mongodb_connection()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "MeEnglishChat is running"}
