from typing import AsyncIterable

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.base import BaseOrm

db_url = "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"


@pytest_asyncio.fixture(scope="function")
async def engine():
    """Создаём engine на всё время тестов"""
    engine = create_async_engine(db_url, future=True, echo=True)

    # создаём таблицы один раз перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine) -> AsyncIterable[AsyncSession]:
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    async with async_session() as session:
        yield session
