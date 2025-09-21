from uuid import UUID

from api.dependencies.services import MediaServiceDep
from fastapi import APIRouter, UploadFile

from app.exceptions.custom_exceptions import UnsupportedMediaTypeError
from app.schemas.file import FileDeleteS

router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


@router.post("/avatar/{user_id}", status_code=201)
async def upload_avatar(
    user_id: UUID, file: UploadFile, media_service: MediaServiceDep
):
    if file.content_type is None:
        raise UnsupportedMediaTypeError(
                message="Invalid file type, file must be an image"
            )
    db_file = await media_service.upload_avatar(file.file, user_id, content_type=file.content_type)
    return {"id": db_file.id, "url": db_file.url}


@router.get("/{file_id}/url")
async def get_file_url(file_id: UUID, media_service: MediaServiceDep):
    file_url = await media_service.get_file_url(file_id)
    return {"url": file_url}


@router.delete("/{file_id}")
async def delete_file(file_id: UUID, schema: FileDeleteS, media_service: MediaServiceDep):
    await media_service.delete_file(file_id=file_id, user_id=schema.user_id)
    return {"message": "File deleted"}
