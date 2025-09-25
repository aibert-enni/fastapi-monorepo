from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import AuthOrm
from app.schemas.auth import AuthS, AuthUpdateRepositoryS


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: AuthS) -> AuthS:
        db_user = AuthOrm(**user.model_dump())
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        return AuthS.model_validate(db_user)
    
    async def update(self, schema: AuthUpdateRepositoryS) -> Optional[AuthS]:
        stmt = select(AuthOrm).where(AuthOrm.id == schema.id)
        result = await self.session.execute(stmt)
        db_user = result.scalars().one_or_none()

        if db_user is None:
            return None
        
        update_data = schema.model_dump(exclude={"id"})
        for key, value in update_data.items():
            if value is None:
                continue
            setattr(db_user, key, value)

        return AuthS.model_validate(db_user)
    
    async def delete(self, id: UUID) -> Optional[AuthS]:
        stmt = select(AuthOrm).where(AuthOrm.id == id)
        result = await self.session.execute(stmt)
        db_user = result.scalars().one_or_none()

        if db_user is not None:
            await self.session.delete(db_user)

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

    async def get_all(self) -> list[AuthS]:
        stmt = select(AuthOrm)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [AuthS.model_validate(db_user) for db_user in db_users]