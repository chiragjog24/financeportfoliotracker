from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

settings = get_settings()


def create_engine():
    return create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=True,
        pool_recycle=settings.database_pool_recycle,
    )


def create_test_engine():
    return create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        poolclass=NullPool,
    )


async_engine = create_engine() if settings.database_url else None

async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
) if async_engine else None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    if async_session_factory is None:
        raise RuntimeError("Database is not configured")

    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> bool:
    if async_engine is None:
        return False

    try:
        async with async_engine.connect() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False


async def init_db() -> None:
    if async_engine is None:
        return
    # Database initialization logic can be added here
    # For now, we rely on Alembic migrations


async def close_db() -> None:
    if async_engine is not None:
        await async_engine.dispose()
