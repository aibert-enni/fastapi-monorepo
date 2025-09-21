import grpc
from google.protobuf import empty_pb2
from proto.auth import auth_pb2_grpc
from proto.media import media_pb2_grpc
from proto.user import user_pb2_grpc

from app.core.settings import settings
from app.schemas.health import HealthCheckS, HealthCheckServiceS, HealthCheckServicesS


class HealthService:
    
    @classmethod
    async def check_auth_service(cls) -> HealthCheckServiceS:
        try:
            async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
                stub = auth_pb2_grpc.AuthStub(channel)

                response = await stub.HealthCheck(empty_pb2.Empty())
            status = response.status
            checks = response.checks
        except grpc.RpcError:
            status = "DOWN"
            checks = {}

        return HealthCheckServiceS(status=status, checks=checks)
    
    @classmethod
    async def check_user_service(cls) -> HealthCheckServiceS:
        try:
            async with grpc.aio.insecure_channel(settings.grpc.user_url) as channel:
                stub = user_pb2_grpc.UserServiceStub(channel)

                response = await stub.HealthCheck(empty_pb2.Empty())
            status = response.status
            checks = response.checks
        except grpc.RpcError:
            status = "DOWN"
            checks = {}

        return HealthCheckServiceS(status=status, checks=checks)

    @classmethod
    async def check_media_service(cls) -> HealthCheckServiceS:
        try:
            async with grpc.aio.insecure_channel(settings.grpc.media_url) as channel:
                stub = media_pb2_grpc.MediaStub(channel)

                response = await stub.HealthCheck(empty_pb2.Empty())
            status = response.status
            checks = response.checks
        except grpc.RpcError:
            status = "DOWN"
            checks = {}

        return HealthCheckServiceS(status=status, checks=checks)
    
    @classmethod
    async def check_services(cls) -> HealthCheckServicesS:
        services = {
            "auth": await cls.check_auth_service(),
            "user": await cls.check_user_service(),
            "media": await cls.check_media_service(),
        }
        status = "healthy" if all(service.status == "healthy" for service in services.values()) else "unhealthy"
        return HealthCheckServicesS(
            status=status,
            auth=await cls.check_auth_service(),
            user= await cls.check_user_service(),
            media=await cls.check_media_service(),
        )
    
    @classmethod 
    async def full_check(cls) -> HealthCheckS:
        services_health = await cls.check_services()
        return HealthCheckS(status=services_health.status, services=services_health)