from pydantic import BaseModel, ConfigDict, EmailStr

from .base import UUIDMixinS


class AuthBaseS(BaseModel):
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class AuthPermissionMixinS(BaseModel):
    is_active: bool = False
    is_superuser: bool = False


class AuthRegisterS(AuthBaseS):
    password: str


class AuthCreateS(AuthBaseS, AuthPermissionMixinS):
    password: str


class AuthRegisterResponseS(AuthBaseS, UUIDMixinS):
    pass


class AuthS(AuthBaseS, AuthPermissionMixinS, UUIDMixinS):
    hashed_password: str
