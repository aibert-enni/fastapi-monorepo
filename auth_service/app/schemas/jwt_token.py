from pydantic import BaseModel


class JWT_TokenS(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenS(BaseModel):
    access_token: str
