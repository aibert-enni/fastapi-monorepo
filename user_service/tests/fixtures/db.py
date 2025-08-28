from typing import AsyncIterable
import asyncpg
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from app.models.base import BaseOrm
from app.service import UserService
from app.repository import UserRepository


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


@pytest_asyncio.fixture(scope="function")
async def user_service(db_session: AsyncSession) -> UserService:

    repo = UserRepository(db_session)
    service = UserService(repo)
    return service
