from typing import Annotated, AsyncIterable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings

engine = create_async_engine(settings.db.URL, pool_pre_ping=True, pool_recycle=3600)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterable[AsyncSession]:
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]