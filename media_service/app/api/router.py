from uuid import UUID

from fastapi import APIRouter, UploadFile

from app.core.dependencies import MediaServiceDep

router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


@router.post("/avatar/{user_id}", status_code=201)
async def upload_avatar(
    user_id: UUID, file: UploadFile, media_service: MediaServiceDep
):
    db_file = await media_service.upload_avatar(file, user_id)
    return {"id": db_file.id, "url": db_file.url}


@router.get("/{file_id}/url")
async def get_file_url(file_id: UUID, media_service: MediaServiceDep):
    file_url = await media_service.get_file_url(file_id)
    return {"url": file_url}


@router.delete("/{file_id}")
async def delete_file(file_id: UUID, media_service: MediaServiceDep):
    await media_service.delete_file(file_id)
    return {"message": "File deleted"}
