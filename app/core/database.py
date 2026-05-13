# Built by AbilitySoft | abilitysoft.net
"""
Async SQLAlchemy engine and session factory.

Provides a single ``async_session_factory`` and a FastAPI dependency
``get_db`` that yields one session per request and ensures cleanup.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

# ── Engine ────────────────────────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_LOG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connection health before checkout
)

# ── Session Factory ───────────────────────────────────────────────
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides a database session.

    The session is automatically closed when the request finishes,
    regardless of whether it succeeded or raised an exception.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
