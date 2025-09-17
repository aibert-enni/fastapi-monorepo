from uuid import UUID

from pydantic import BaseModel


class UUIDMixinS(BaseModel):
    id: UUID
