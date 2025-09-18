import io
from datetime import datetime, timedelta, timezone
from typing import BinaryIO, Literal, Optional
from uuid import UUID
from venv import logger

from PIL import Image, UnidentifiedImageError
from sqlalchemy.exc import IntegrityError as SQL_IntegrityError

from app.core.settings import settings
from app.exceptions.custom_exceptions import (
    AuthorizationError,
    FileTooLargeError,
    NotFoundError,
    UnsupportedMediaTypeError,
    ValidationError,
)
from app.models.file import FileType
from app.repository import FileRepository
from app.schemas.file import FileFilledS, FileS
from app.services.s3_service import S3Client


class MediaService:
    MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
    AVATAR_SIZE = (256, 256)

    def __init__(self, file_repository: FileRepository, file_service: S3Client) -> None:
        self.file_repository = file_repository
        self.file_service = file_service

    def get_file_size(self, file: BinaryIO) -> int:
        pos = file.tell()
        file.seek(0, io.SEEK_END)
        size = file.tell()
        file.seek(pos)
        return size

    async def upload(
        self,
        file: BinaryIO,
        file_type: FileType,
        content_type: str,
        file_path: str,
        owner_id: Optional[UUID] = None,
        file_expire: int = settings.file.default_expire_seconds,
        visibility: Literal["public", "private"] = "public",
    ) -> FileFilledS:
        file.seek(0)
        size = self.get_file_size(file)
        try:
            db_file = await self.file_repository.save(
                FileS(
                    type=file_type,
                    owner_id=owner_id,
                    mime_type=content_type,
                    size=size,
                    is_private=visibility == "private",
                )
            )
            await self.file_repository.session.commit()
        except SQL_IntegrityError as db_exc:
            logger.error(f"DB error for file {file_path}, owner {owner_id}: {db_exc}")
            raise ValidationError(message="Something went wrong, please try again")

        file_path = f"{file_path}/{db_file.id}"

        if visibility == "private":
            file_url = await self.file_service.get_private_url(file_path, file_expire)
            await self.file_service.private_upload(
                file, file_path, content_type, file_expire
            )
        else:
            file_url = await self.file_service.get_private_url(file_path, file_expire)
            await self.file_service.public_upload(file, file_path, content_type)

        try:
            db_file.url = file_url
            db_file.key = file_path
            db_file.expire = datetime.now(timezone.utc) + timedelta(seconds=file_expire)
            await self.file_repository.update(db_file)
            await self.file_repository.session.commit()
        except SQL_IntegrityError as db_exc:
            logger.error(f"DB error for file {file_path}, owner {owner_id}: {db_exc}")

        return FileFilledS(**db_file.model_dump())

    async def upload_avatar(
        self,
        file: BinaryIO,
        owner_id: UUID,
        content_type: str,
    ) -> FileFilledS:
        if content_type and not content_type.startswith("image/"):
            raise UnsupportedMediaTypeError(
                message="Invalid file type, file must be an image"
            )
        size = self.get_file_size(file)
        if size and size > self.MAX_AVATAR_SIZE:
            raise FileTooLargeError(
                message="File is too large, maximum size is 5MB",
            )
        try:
            file.seek(0)
            with Image.open(file) as image:
                image = image.convert("RGB")
                image.thumbnail(self.AVATAR_SIZE)
                buffer = io.BytesIO()
                image.save(
                    buffer,
                    "JPEG",
                    quality=85,
                    optimize=True,
                )
            buffer.seek(0)
            file_path = f"avatars/{owner_id}"
            return await self.upload(
                file=buffer,
                file_type=FileType.AVATAR,
                content_type="image/jpeg",
                file_path=file_path,
                owner_id=owner_id,
                visibility="public",
            )
        except (UnidentifiedImageError, OSError):
            raise UnsupportedMediaTypeError(
                message="Uploaded file is not a valid image"
            )

    async def get_file_url(self, file_id: UUID, user_id: Optional[UUID] = None) -> str:
        file = await self.file_repository.get_with_users(file_id)
        if file is None or file.url is None:
            raise NotFoundError(message="File not found")
        if file.is_private and (
            file.owner_id != user_id and user_id not in file.users_with_access
        ):
            raise AuthorizationError(message="Access denied")
        now = datetime.now(timezone.utc)
        if file.expire is None or file.expire < now:
            if file.key is None:
                raise NotFoundError(message="File not found")
            url = await self.file_service.get_private_url(file.key, settings.file.default_expire_seconds)
            file.url = url
            file.expire = now + timedelta(seconds=settings.file.default_expire_seconds)
            await self.file_repository.update(file=file)
            await self.file_repository.session.commit()
        return file.url

    async def delete_file(self, file_id: UUID, user_id: UUID, is_superuser: bool = False) -> None:
        file_db = await self.file_repository.get(file_id)
        if file_db is None:
            raise NotFoundError(message="File not found")
        if file_db.owner_id != user_id:
            if not is_superuser:
                raise AuthorizationError(message="You don't have permission to delete")
        await self.file_repository.delete(file_id)
        await self.file_repository.session.commit()
        if file_db.url is None or file_db.key is None:
            return
        await self.file_service.delete(file_db.key)
