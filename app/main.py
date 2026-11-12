from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1 import items as items_router
from app.config import settings
from app.database import AsyncSessionLocal, create_tables

logger = logging.getLogger(__name__)


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle events."""
    logger.info("Starting up %s v%s", settings.app_name, settings.app_version)
    await create_tables()
    yield
    logger.info("Shutting down %s", settings.app_name)


# ── App factory ───────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router.router, prefix="/api/v1")


# ── Health / readiness endpoints ──────────────────────────────────────────────

@app.get("/health", tags=["ops"])
async def health():
    """Liveness probe — always returns 200 if the process is alive."""
    return {"status": "ok"}


@app.get("/status", tags=["ops"])
async def status():
    """Shallow status of subsystems (no live DB query)."""
    return {
        "api": "up",
        "db": "connected",
        "worker": "unknown",
    }


@app.get("/ready", tags=["ops"])
async def ready():
    """Readiness probe — verifies the DB is reachable."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "db": "ok"}
    except Exception as exc:  # noqa: BLE001
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=f"DB not ready: {exc}") from exc
