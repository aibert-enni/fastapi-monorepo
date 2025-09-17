from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.core.db import session_maker
from app.repository import FileRepository
from app.services.media_service import MediaService
from app.services.s3_service import s3_client


@asynccontextmanager
async def get_media_service() -> AsyncIterator[MediaService]:
    async with session_maker() as db:
        file_repository = FileRepository(db)
        yield MediaService(file_repository, s3_client)