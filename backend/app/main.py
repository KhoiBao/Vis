from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.quadrilateral import router
from app.core.config import settings


# backend/app/main.py -> project root (Vis)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

FRONTEND_FILE = PROJECT_ROOT / "test.html"


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


app.add_middleware(
    CORSMiddleware,

    # Development only.
    # Khi deploy nên thay bằng domain frontend thực tế.
    allow_origins=["*"],

    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================================================
# FRONTEND
# Mở http://127.0.0.1:8000/app để dùng demo
# =========================================================

@app.get("/app", include_in_schema=False)
def frontend():

    if not FRONTEND_FILE.exists():
        return {
            "status": "error",
            "detail": "test.html not found",
            "path": str(FRONTEND_FILE)
        }

    return FileResponse(FRONTEND_FILE)


@app.get("/health/neo4j")
def neo4j_health():

    from app.services.neo4j.repository import (
        Neo4jRepository
    )

    repository = Neo4jRepository()

    try:

        repository.verify_connection()

        return {
            "status": "ok",
            "neo4j": "connected"
        }

    except Exception as exc:

        return {
            "status": "error",
            "neo4j": "disconnected",
            "detail": str(exc)
        }

    finally:
        repository.close()