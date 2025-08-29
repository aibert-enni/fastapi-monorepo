from uuid import UUID

from pydantic import BaseModel


class UserS(BaseModel):
    id: UUID
    username: str
    fullname: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
