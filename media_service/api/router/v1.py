from fastapi import APIRouter

from .router import router as media_router

router = APIRouter(prefix="/v1")

router.include_router(media_router)
