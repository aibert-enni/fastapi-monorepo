from uuid import UUID

from fastapi import APIRouter, UploadFile

from app.core.dependencies import MediaServiceDep
from app.models.file import FileType

router = APIRouter(
    prefix="/media",
    tags=["media"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload/document", status_code=201)
async def upload_file(file: UploadFile, media_service: MediaServiceDep):
    file_url = await media_service.upload(file, FileType.DOCUMENT, None)
    return {"url": file_url}


@router.post("/upload/avatar/{user_id}", status_code=201)
async def upload_avatar(
    user_id: UUID, file: UploadFile, media_service: MediaServiceDep
):
    file_url = await media_service.upload(file, FileType.DOCUMENT, user_id)
    return {"url": file_url}
