from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import AuthOrm
from app.schemas.auth import AuthS


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: AuthS) -> AuthS:
        db_user = AuthOrm(**user.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return AuthS.model_validate(db_user)

    async def get_by_username(self, username: str) -> Optional[AuthS]:
        stmt = select(AuthOrm).where(AuthOrm.username == username)
        result = await self.session.execute(stmt)
        db_user = result.scalars().one_or_none()
        return AuthS.model_validate(db_user) if db_user else None

    async def get_by_id(self, id: UUID) -> Optional[AuthS]:
        stmt = select(AuthOrm).where(AuthOrm.id == id)
        result = await self.session.execute(stmt)
        db_user = result.scalars().one_or_none()
        return AuthS.model_validate(db_user) if db_user else None
