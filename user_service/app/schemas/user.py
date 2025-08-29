from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseS(BaseModel):
    username: str
    fullname: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreateS(UserBaseS):
    password: str
    is_active: bool = False
    is_superuser: bool = False


class UserS(UserCreateS):
    id: UUID
