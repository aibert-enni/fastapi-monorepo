
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import FileOrm
from app.schemas.file import FileS


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, file: FileS) -> FileS:
        file_db = FileOrm(**file.model_dump())
        self.session.add(file_db)
        await self.session.commit()
        await self.session.refresh(file_db)
        return FileS.model_validate(file_db)
