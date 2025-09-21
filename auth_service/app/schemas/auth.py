from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .base import UUIDMixinS


class AuthBaseS(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr = Field(..., min_length=1)

    model_config = ConfigDict(from_attributes=True)


class AuthPermissionMixinS(BaseModel):
    is_active: bool = False
    is_superuser: bool = False


class AuthRegisterS(AuthBaseS):
    password: str = Field(..., min_length=1)


class AuthLoginS(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class AuthCreateS(AuthBaseS, AuthPermissionMixinS):
    password: str = Field(..., min_length=1)


class AuthRegisterResponseS(AuthBaseS, UUIDMixinS):
    pass


class AuthS(AuthBaseS, AuthPermissionMixinS, UUIDMixinS):
    hashed_password: str = Field(..., min_length=1)

class AuthUpdateS(BaseModel):
    username: Optional[str] = Field(min_length=1, default=None)
    email: Optional[EmailStr] = Field(min_length=1, default=None)
    password: Optional[str] = Field(min_length=1, default=None)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class AuthUpdateRepositoryS(UUIDMixinS):
    username: Optional[str] = Field(min_length=1, default=None)
    email: Optional[EmailStr] = Field(min_length=1, default=None)
    hashed_password: Optional[str] = Field(min_length=1, default=None)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None