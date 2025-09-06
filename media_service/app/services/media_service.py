import io
from typing import Optional
from uuid import UUID

from fastapi import UploadFile

from app.models.file import FileType
from app.repository import FileRepository
from app.schemas.file import FileS
from app.services.s3_service import S3Client


class MediaService:
    def __init__(self, file_repository: FileRepository, file_service: S3Client) -> None:
        self.file_repository = file_repository
        self.file_service = file_service

    async def upload(
        self,
        file: UploadFile,
        type: FileType,
        owner_id: Optional[UUID] = None,
    ) -> str:
        file_binary = file.file
        file_binary.seek(0)
        body = io.BytesIO(file_binary.read())
        content_type = f"{file.content_type}"
        file_name = f"{file.filename}"
        if type == FileType.AVATAR:
            file_name = f"{owner_id}.jpg"
        file_path = f"{type.name}/{file_name}"
        file_url = await self.file_service.upload(body, file_path, content_type)
        size = file.size if file.size else 0
        try:
            await self.file_repository.save(
                FileS(
                    url=file_url,
                    type=type,
                    owner_id=owner_id,
                    mime_type=content_type,
                    size=size,
                )
            )
        except Exception as e:
            print(e)
        return file_url
