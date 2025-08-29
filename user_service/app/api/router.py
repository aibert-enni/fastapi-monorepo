from fastapi import APIRouter

from app.core.dependencies import UserServiceDep
from app.schemas.user import UserCreateS, UserS

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=UserS)
async def create_user(user: UserCreateS, user_service: UserServiceDep):
    user = await user_service.create_user(user)
    return user
