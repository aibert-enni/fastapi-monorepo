from fastapi import APIRouter

from .auth import router as auth_router

router = APIRouter(prefix="/admin", tags=["admin"])

router.include_router(auth_router)