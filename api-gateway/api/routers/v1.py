from fastapi import APIRouter

from .auth import router as user_router
from .media import router as media_router

router = APIRouter(prefix="/v1")

router.include_router(user_router)
router.include_router(media_router)
