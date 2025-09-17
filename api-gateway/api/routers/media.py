import io
from uuid import UUID

import grpc
from api.dependencies.current_user import GetCurrentUserDep
from fastapi import APIRouter, UploadFile, status
from proto.media import media_pb2, media_pb2_grpc

from app.core.settings import settings
from app.exceptions.custom_exceptions import APIError
from app.schemas.media import FileUploadResponseS, GetFileUrlResponse

router = APIRouter(prefix="/files", tags=["media"])

@router.post("/upload/avatar")
async def upload_avatar(file: UploadFile, user: GetCurrentUserDep) -> FileUploadResponseS:
    if file.content_type is None:
        raise Exception
    MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
    file.file.seek(0, io.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_AVATAR_SIZE:
        raise APIError(
                grpc_code=grpc.StatusCode.INVALID_ARGUMENT,
                http_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                message="File is too large, maximum size is 5MB",
            )
    async with grpc.aio.insecure_channel(settings.grpc.media_url) as channel:
        stub = media_pb2_grpc.MediaStub(channel)
        request = media_pb2.UploadAvatarRequest(owner_id=str(user.id), file=file.file.read(), content_type=file.content_type)
        response = await stub.UploadAvatar(request)

    return FileUploadResponseS(id=response.id, url=response.url)

@router.get("/{file_id}/url")
async def get_file_url(file_id: UUID) -> GetFileUrlResponse:
    async with grpc.aio.insecure_channel(settings.grpc.media_url) as channel:
        stub = media_pb2_grpc.MediaStub(channel)
        request = media_pb2.GetFileUrlRequest(id=str(file_id))
        response = await stub.GetFileUrl(request)
    
    return GetFileUrlResponse(url=response.url)

@router.delete("/{file_id}")
async def delete_file(file_id: UUID, user: GetCurrentUserDep) -> dict:
    async with grpc.aio.insecure_channel(settings.grpc.media_url) as channel:
        stub = media_pb2_grpc.MediaStub(channel)
        request = media_pb2.DeleteFileRequest(file_id=str(file_id), user_id=str(user.id), is_superuser=user.is_superuser)
        response = await stub.DeleteFile(request)
    return {"status": response.success}