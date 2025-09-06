import enum
from uuid import UUID

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseOrm
from app.models.mixins import CreateAtMixin, UpdateAtMixin, UuidPkMixin


class FileType(str, enum.Enum):
    AVATAR = "avatar"
    DOCUMENT = "document"
    OTHER = "other"


class FileOrm(BaseOrm, UuidPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "files"

    owner_id: Mapped[UUID] = mapped_column(nullable=True)
    type: Mapped[FileType] = mapped_column(
        PGEnum(FileType, name="file_type"), nullable=False, default=FileType.OTHER
    )
    mime_type: Mapped[str] = mapped_column(String(64), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(String(256), nullable=False)
