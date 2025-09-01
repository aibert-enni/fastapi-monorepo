from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserBaseS(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateS(UserBaseS):
    id: Optional[UUID] = None


class UserUpdateS(UserBaseS):
    pass


class UserS(UserBaseS):
    id: Optional[UUID] = None
