from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import UUIDMixinS


class AuthS(UUIDMixinS):
    username: str
    email: str
    is_active: bool
    is_superuser: bool

class AuthMeResponse(UUIDMixinS):
    username: str

class AuthRegisterRequestS(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=8)

class AuthRegisterResponseS(UUIDMixinS):
    username: str

class AuthLoginRequestS(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class AuthLoginResponseS(BaseModel):
    access_token: str

class RefreshAccessTokenResponse(BaseModel):
    access_token: str

class CreateUserByAdminRequest(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr = Field(..., min_length=1)
    password: str
    is_active: bool = False
    is_superuser: bool = False

class CreateUserByAdminResponse(UUIDMixinS):
    username: str
    email: str
    is_active: bool
    is_superuser: bool


class UpdateUserByAdminRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class UpdateUserByAdminResponse(UUIDMixinS):
    username: str
    email: str
    is_active: bool
    is_superuser: bool


class DeleteUserByAdminResponse(BaseModel):
    id: str
    is_deleted: bool