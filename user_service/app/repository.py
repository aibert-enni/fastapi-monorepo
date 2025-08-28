from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserOrm
from app.schemas.user import UserS


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: UserS) -> UserOrm:
        db_user = UserOrm(**user.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user
