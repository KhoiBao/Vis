from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.quadrilateral import router
from app.core.config import settings


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