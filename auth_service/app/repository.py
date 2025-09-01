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
