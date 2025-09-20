from app.schemas.base import UUIDMixinS


class AuthS(UUIDMixinS):
    username: str
    email: str
    is_active: bool
    is_superuser: bool

class BaseAuth(UUIDMixinS):
    username: str

