from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthBaseS(BaseModel):
    user_id: UUID
    is_active: bool = False
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class AuthCreateS(AuthBaseS):
    password: str


class AuthS(AuthBaseS):
    id: Optional[UUID] = None
    hashed_password: str
