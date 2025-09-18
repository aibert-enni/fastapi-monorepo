import asyncio
import io
import logging
from concurrent import futures
from uuid import UUID

import grpc
from proto import media_pb2, media_pb2_grpc

from app.core.settings import settings
from app.exceptions.custom_exceptions import ValidationError
from rpc.dependencies.services import get_media_service
from rpc.interceptors.exception_handler import ErrorInterceptor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

class AuthServicer(media_pb2_grpc.MediaServicer):
    async def UploadAvatar(self, request, context):
        async with get_media_service() as media_service:
            file = await media_service.upload_avatar(file=io.BytesIO(request.file), owner_id=request.owner_id, content_type=request.content_type)
        return media_pb2.UploadAvatarResponse(id=str(file.id), url=file.url)
    
    async def GetFileUrl(self, request, context):
        async with get_media_service() as media_service:
            url = await media_service.get_file_url(file_id=request.id)
        return media_pb2.GetFileUrlResponse(url=url)
    
    async def DeleteFile(self, request, context):
        try:
            file_id = request.file_id
        except Exception:
            raise ValidationError(message="file id format is invalid")
        
        try:
            user_id = UUID(request.user_id)
        except Exception:
            raise ValidationError(message="user id format is invalid")
        async with get_media_service() as media_service:
            await media_service.delete_file(file_id=file_id, user_id=user_id, is_superuser=request.is_superuser)
        return media_pb2.DeleteFileResponse(status="success")
    

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=4), interceptors=[ErrorInterceptor()])
    media_pb2_grpc.add_MediaServicer_to_server(servicer=AuthServicer(), server=server)
    server.add_insecure_port(f"[::]:{settings.grpc.port}")
    logger.info(f"Server address: localhost:{settings.grpc.port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())