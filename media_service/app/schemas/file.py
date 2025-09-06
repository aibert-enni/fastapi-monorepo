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
    url: str

    model_config = ConfigDict(from_attributes=True)
