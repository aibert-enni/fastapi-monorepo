from typing import Annotated

from fastapi import Depends

from app.core.db import SessionDep
from app.repository import FileRepository
from app.services.media_service import MediaService
from app.services.s3_service import s3_client


def get_file_repository(db: SessionDep) -> FileRepository:
    return FileRepository(db)


def get_media_service(
    file_repository: FileRepository = Depends(get_file_repository),
) -> MediaService:
    return MediaService(file_repository=file_repository, file_service=s3_client)


FileRepositoryDep = Annotated[FileRepository, Depends(get_file_repository)]
MediaServiceDep = Annotated[MediaService, Depends(get_media_service)]
