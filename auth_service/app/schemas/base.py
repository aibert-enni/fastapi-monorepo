from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UUIDMixinS(BaseModel):
    id: Optional[UUID] = None
