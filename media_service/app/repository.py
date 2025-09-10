from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.file import FileOrm
from app.schemas.file import FileS, FileWithUsersS


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, file: FileS) -> FileS:
        file_db = FileOrm(**file.model_dump())
        self.session.add(file_db)
        await self.session.flush()
        await self.session.refresh(file_db)
        return FileS.model_validate(file_db)

    async def update(self, file: FileS) -> None:
        stmt = (
            update(FileOrm)
            .where(FileOrm.id == file.id)
            .values(**file.model_dump(exclude={"id"}))
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.flush()

    async def delete(self, file_id: UUID) -> None:
        stmt = delete(FileOrm).where(FileOrm.id == file_id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def get(self, file_id: UUID) -> Optional[FileS]:
        stmt = select(FileOrm).where(FileOrm.id == file_id)
        result = await self.session.execute(stmt)
        db_file = result.scalars().one_or_none()
        return FileS.model_validate(db_file) if db_file else None

    async def get_with_users(self, file_id: UUID) -> Optional[FileWithUsersS]:
        stmt = (
            select(FileOrm)
            .options(selectinload(FileOrm.users_with_access))
            .where(FileOrm.id == file_id)
        )
        result = await self.session.execute(stmt)
        db_file = result.scalars().one_or_none()

        if db_file is None:
            return None

        users_with_access = [u.user_id for u in db_file.users_with_access]

        file_schema = FileWithUsersS(
            id=db_file.id,
            owner_id=db_file.owner_id,
            type=db_file.type,
            mime_type=db_file.mime_type,
            size=db_file.size,
            url=db_file.url,
            key=db_file.key,
            is_private=db_file.is_private,
            users_with_access=users_with_access,
        )

        return file_schema

    async def get_url(self, file_id: UUID) -> Optional[str]:
        stmt = select(FileOrm.url).where(FileOrm.id == file_id)
        result = await self.session.execute(stmt)
        file_url = result.scalars().one_or_none()
        return file_url if file_url else None
