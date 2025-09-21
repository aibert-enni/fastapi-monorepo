from typing import Optional

from app.schemas.base import UUIDMixinS


class UserS(UUIDMixinS):
    first_name: Optional[str] = None
    last_name: Optional[str] = None