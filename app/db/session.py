from functools import lru_cache
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from settings import settings


@lru_cache
def get_engine():
    kwargs = dict(url=settings.PG_URL, echo=False)
    if "sqlite" not in settings.PG_URL:
        kwargs.update(pool_pre_ping=True, pool_size=10, max_overflow=20)
    return create_async_engine(**kwargs)


def get_session_factory():
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@asynccontextmanager
async def LocalSession():
    factory = get_session_factory()
    async with factory() as session:
        yield session


async def get_db():
    async with LocalSession() as session:
        yield session
