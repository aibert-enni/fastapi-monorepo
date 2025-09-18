import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import FileRepository
from app.services.media_service import MediaService
from app.services.s3_service import s3_client


@pytest_asyncio.fixture(scope="function")
async def media_service(db_session: AsyncSession) -> MediaService:
    repo = FileRepository(db_session)
    service = MediaService(file_repository=repo, file_service=s3_client)
    return service
