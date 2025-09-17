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