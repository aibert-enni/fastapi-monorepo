from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.file import FileType


class FileS(BaseModel):
    id: Optional[UUID] = None
    owner_id: Optional[UUID] = None
    type: FileType
    mime_type: str
    size: int
    url: Optional[str] = None
    key: Optional[str] = None
    is_private: bool

    model_config = ConfigDict(from_attributes=True)

class FileFilledS(BaseModel):
    id: UUID
    owner_id: Optional[UUID] = None
    type: FileType
    mime_type: str
    size: int
    url: str
    key: str
    is_private: bool

    model_config = ConfigDict(from_attributes=True)

class FileWithUsersS(FileS):
    users_with_access: list[UUID]
