import asyncio
import logging
from concurrent import futures
from uuid import UUID

import grpc
from proto import user_pb2, user_pb2_grpc

from app.core.db import session_maker
from app.core.settings import settings
from app.exceptions.custom_exceptions import ValidationError
from app.schemas.user import UserCreateS, UserUpdateS
from app.services.brokers.rabbit.main import rabbit_service
from app.services.health_service import HealthService
from app.core.dependencies import get_user_service
from rpc.interceptors.exception_handler import ErrorInterceptor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

class UserServer(user_pb2_grpc.UserServiceServicer):
    async def CreateUser(self, request: user_pb2.CreateUserRequest, context):
        async with get_user_service() as user_service:
            try:
                id = UUID(request.id)
            except (ValueError, TypeError, AttributeError):
                raise ValidationError(message="user id format is invalid")
            
            user = await user_service.create_user(UserCreateS(id=id, first_name=request.first_name, last_name=request.last_name))

        return user_pb2.CreateUserResponse(id=str(user.id), first_name=user.first_name, last_name=user.last_name)

    async def UpdateUser(self, request: user_pb2.UpdateUserRequest, context):
        async with get_user_service() as user_service:
            try:
                id = UUID(request.id)
            except (ValueError, TypeError, AttributeError):
                raise ValidationError(message="user id format is invalid")
            user = await user_service.update_user(UserUpdateS(id=id, first_name=request.first_name, last_name=request.last_name))
        return user_pb2.UpdateUserResponse(id=str(user.id), first_name=user.first_name, last_name=user.last_name)
    
    async def HealthCheck(self, request, context):
        async with session_maker() as db:
            heatlth_service = HealthService(db_session=db, broker_service=rabbit_service)
            health = await heatlth_service.health_check()
        return user_pb2.HealthCheckResponse(status=health.status, checks=health.checks)
    
async def serve():
    await rabbit_service.start()
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=4), interceptors=[ErrorInterceptor()])
    user_pb2_grpc.add_UserServiceServicer_to_server(servicer=UserServer(), server=server)
    server.add_insecure_port(f"[::]:{settings.grpc.port}")
    logger.info(f"Server address: localhost:{settings.grpc.port}")
    try:
        await server.start()
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(grace=5)
    finally:
        await rabbit_service.stop()

if __name__ == "__main__":
    asyncio.run(serve())