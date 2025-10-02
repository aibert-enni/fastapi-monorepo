import asyncio
import logging
from concurrent import futures
import time

import grpc
from prometheus_client import start_http_server

from rpc.interceptors.promotheus_handler import PromotheusInterceptor
from proto import auth_pb2, auth_pb2_grpc
from rpc.interceptors.exception_handler import ErrorInterceptor

from app.core.db import session_maker
from app.core.dependencies import get_auth_service
from app.core.settings import settings
from app.core.setup import setup
from app.exceptions.custom_exceptions import CredentialError
from app.schemas.auth import AuthCreateS, AuthLoginS, AuthUpdateS
from app.services.brokers.broker_manager import BrokersType, get_broker_manager
from app.services.health_service import HealthService

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
            broker_manager = get_broker_manager()
            health_service = HealthService(db_session=db, broker_service=broker_manager.get_broker())
            health = await health_service.health_check()
        return auth_pb2.HealthCheckResponse(status=health.status, checks=health.checks)
    
    async def CreateUserByAdmin(self, request, context):
        async with get_auth_service() as auth_service:
            user = await auth_service.create_auth_by_admin(access_token=request.access_token, schema=AuthCreateS(username=request.username, email=request.email, password=request.password, is_active=request.is_active, is_superuser=request.is_superuser))
        return auth_pb2.CreateUserByAdminResponse(id=str(user.id), username=user.username, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser)
    
    async def UpdateUserByAdmin(self, request, context):
        async with get_auth_service() as auth_service:
            user = await auth_service.update_auth_by_admin(access_token=request.access_token, user_id=request.id, schema=AuthUpdateS(username=request.username, email=request.email, password=request.password, is_active=request.is_active, is_superuser=request.is_superuser))
        return auth_pb2.UpdateUserByAdminResponse(id=str(user.id), username=user.username, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser)
    
    async def DeleteUserByAdmin(self, request, context):
        async with get_auth_service() as auth_service:
            await auth_service.delete_auth_by_admin(access_token=request.access_token, user_id=request.id)
        return auth_pb2.DeleteUserByAdminResponse(id=request.id, is_deleted=True)
    
    async def GetAllUsersByAdmin(self, request, context):
        async with get_auth_service() as auth_service:
            users = await auth_service.get_all_auths_by_admin(access_token=request.access_token)
        users = [auth_pb2.User(**user.model_dump(mode="json", exclude={"hashed_password"})) for user in users]
        return auth_pb2.GetAllUsersByAdminResponse(users=users)

async def serve():
    if settings.rabbit.ENABLE:
        await get_broker_manager().initalize(BrokersType.RABBIT)
    else:
        await get_broker_manager().initalize(BrokersType.DUMMY)
    await setup()
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=4), interceptors=[PromotheusInterceptor(), ErrorInterceptor()])
    auth_pb2_grpc.add_AuthServicer_to_server(servicer=AuthServicer(), server=server)
    server.add_insecure_port(f"[::]:{settings.grpc.port}")
    logger.info(f"Server address: localhost:{settings.grpc.port}")
    await server.start()

    start_http_server(port=8888)

    await server.wait_for_termination()
    await get_broker_manager().shutdown()

if __name__ == "__main__":
    asyncio.run(serve())