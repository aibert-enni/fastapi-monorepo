from fastapi import APIRouter

from app.schemas.health import HealthCheckServiceS, HealthCheckS
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/auth",)
async def check_auth() -> HealthCheckServiceS:
    response = await HealthService.check_auth_service()
    return response

@router.get("/user",)
async def check_user() -> HealthCheckServiceS:
    response = await HealthService.check_user_service()
    return response

@router.get("/media",)
async def check_media() -> HealthCheckServiceS:
    response = await HealthService.check_media_service()
    return response

@router.get("/", tags=["health"])
async def check_health() -> HealthCheckS:
    response = await HealthService.check_services()
    return HealthCheckS(status="healthy", services=response)