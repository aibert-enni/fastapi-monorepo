from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseS(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    is_active: bool = False
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserS(UserBaseS):
    id: Optional[UUID] = None
    hashed_password: str


class UserCreateS(UserBaseS):
    password: str
