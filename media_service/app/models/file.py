import enum
from uuid import UUID

from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=True)
    key: Mapped[str] = mapped_column(Text, unique=True, nullable=True)

    is_private: Mapped[bool] = mapped_column(
        Boolean, server_default="false", default=False, nullable=False
    )

    users_with_access: Mapped[list["UserFileAccess"]] = relationship(
        "UserFileAccess", back_populates="file"
    )


class UserFileAccess(BaseOrm, UuidPkMixin, CreateAtMixin, UpdateAtMixin):
    __tablename__ = "users_files_access"

    user_id: Mapped[UUID] = mapped_column(nullable=False)
    file_id: Mapped[UUID] = mapped_column(
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
    )

    file: Mapped["FileOrm"] = relationship(
        "FileOrm", back_populates="users_with_access"
    )

    __table_args__ = (UniqueConstraint("user_id", "file_id", name="uq_user_file"),)
