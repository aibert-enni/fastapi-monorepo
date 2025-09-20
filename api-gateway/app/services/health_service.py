import grpc
from google.protobuf import empty_pb2

from app.schemas.health import HealthCheckServiceS, HealthCheckServicesS
from app.core.settings import settings
from proto.auth import auth_pb2_grpc
from proto.user import user_pb2_grpc
from proto.media import media_pb2_grpc

class HealthService:
    
    @classmethod
    async def check_auth_service(cls) -> HealthCheckServiceS:
        async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
            stub = auth_pb2_grpc.AuthStub(channel)

            response = await stub.HealthCheck(empty_pb2.Empty())

        return HealthCheckServiceS(status=response.status, checks=response.checks)
    
    @classmethod
    async def check_user_service(cls) -> HealthCheckServiceS:
        async with grpc.aio.insecure_channel(settings.grpc.user_url) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            response = await stub.HealthCheck(empty_pb2.Empty())
        return HealthCheckServiceS(status=response.status, checks=response.checks)

    @classmethod
    async def check_media_service(cls) -> HealthCheckServiceS:
        async with grpc.aio.insecure_channel(settings.grpc.media_url) as channel:
            stub = media_pb2_grpc.MediaStub(channel)
            response = await stub.HealthCheck(empty_pb2.Empty())
        return HealthCheckServiceS(status=response.status, checks=response.checks)
    
    @classmethod
    async def check_services(cls) -> HealthCheckServicesS:
        return HealthCheckServicesS(
            auth=await cls.check_auth_service(),
            user= await cls.check_user_service(),
            media=await cls.check_media_service(),
        )