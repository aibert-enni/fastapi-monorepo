from fastapi import APIRouter, Depends

from api.dependencies.current_user import get_current_superuser
from app.schemas.health import HealthCheckServiceS, HealthCheckS
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def ping():
    return {"ping": "pong"}

@router.get("/services/auth", dependencies=[Depends(get_current_superuser)])
async def check_auth() -> HealthCheckServiceS:
    response = await HealthService.check_auth_service()
    return response

@router.get("/services/user", dependencies=[Depends(get_current_superuser)])
async def check_user() -> HealthCheckServiceS:
    response = await HealthService.check_user_service()
    return response

@router.get("/services/media", dependencies=[Depends(get_current_superuser)])
async def check_media() -> HealthCheckServiceS:
    response = await HealthService.check_media_service()
    return response

@router.get("/full", dependencies=[Depends(get_current_superuser)])
async def check_full_health() -> HealthCheckS:
    response = await HealthService.check_services()
    return HealthCheckS(status="healthy", services=response)