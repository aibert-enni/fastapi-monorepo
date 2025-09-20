from typing import Optional
from pydantic import BaseModel


class UserUpdateRequestS(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None