import asyncio
import logging
from concurrent import futures

import grpc
from app.services.health_service import HealthService
from proto import auth_pb2, auth_pb2_grpc
from rpc.dependencies.services import get_auth_service
from rpc.interceptors.exception_handler import ErrorInterceptor

from app.core.settings import settings
from app.core.db import session_maker
from app.exceptions.custom_exceptions import CredentialError
from app.schemas.auth import AuthCreateS, AuthLoginS
from app.services.brokers.rabbit.main import rabbit_broker_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

class AuthServicer(auth_pb2_grpc.AuthServicer):
    async def RegisterUser(self, request, context):
        async with get_auth_service() as auth_service:
            auth = await auth_service.create_auth(AuthCreateS(username=request.username, email=request.email, password=request.password, is_active=True, is_superuser=False))
        return auth_pb2.AuthRegisterResponse(id=str(auth.id), username=auth.username, email=auth.email)
    
    async def LoginUser(self, request, context):
        async with get_auth_service() as auth_service:
            tokens = await auth_service.login_user(AuthLoginS(username=request.username, password=request.password))
        return auth_pb2.AuthLoginResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)
    
    async def RefreshAccessToken(self, request, context):
        async with get_auth_service() as auth_service:
            access_token = await auth_service.refresh_access_token(payload=request.payload)
        return auth_pb2.RefreshAccessTokenResponse(access_token=access_token)
    
    async def CurrentUser(self, request, context):
        async with get_auth_service() as auth_service:
            user = await auth_service.get_auth_by_token(payload=request.payload)
        if user is None:
            raise CredentialError
        user_message = auth_pb2.User(**user.model_dump(mode="json", exclude={"hashed_password"}))
        return auth_pb2.CurrentUserResponse(user=user_message)
    
    async def HealthCheck(self, request, context):
        async with session_maker() as db:
            health_service = HealthService(db_session=db, broker_service=rabbit_broker_service)
            health = await health_service.health_check()
        return auth_pb2.HealthCheckResponse(status=health.status, checks=health.checks)

    

async def serve():
    await rabbit_broker_service.start()
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=4), interceptors=[ErrorInterceptor()])
    auth_pb2_grpc.add_AuthServicer_to_server(servicer=AuthServicer(), server=server)
    server.add_insecure_port(f"[::]:{settings.grpc.port}")
    logger.info(f"Server address: localhost:{settings.grpc.port}")
    await server.start()
    await server.wait_for_termination()
    await rabbit_broker_service.stope()

if __name__ == "__main__":
    asyncio.run(serve())