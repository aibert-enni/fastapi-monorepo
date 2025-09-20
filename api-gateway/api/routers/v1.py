from fastapi import APIRouter

from .auth import router as auth_router
from .media import router as media_router
from .user import router as user_router
from .health import router as health_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(media_router)
router.include_router(user_router)
router.include_router(health_router)