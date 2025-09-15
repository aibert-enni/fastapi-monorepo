from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserOrm
from app.schemas.user import UserS


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserS) -> UserS:
        db_user = UserOrm(**user.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return UserS.model_validate(db_user)

    async def update(self, user: UserS) -> Optional[UserS]:
        stmt = (
            update(UserOrm)
            .where(UserOrm.id == user.id)
            .values(**user.model_dump(exclude={"id"}))
            .returning(UserOrm)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        db_user = result.scalars().one_or_none()
        return UserS.model_validate(db_user) if db_user else None
