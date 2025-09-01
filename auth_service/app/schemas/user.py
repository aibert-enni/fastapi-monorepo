from uuid import UUID

from pydantic import BaseModel


class UserS(BaseModel):
    id: UUID
