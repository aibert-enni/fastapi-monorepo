from fastapi import APIRouter

from app.core.dependencies import UserServiceDep
from app.schemas.user import UserBaseS, UserCreateS

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=UserBaseS)
async def create_user(user: UserCreateS, user_service: UserServiceDep):
    user = await user_service.create_user(user)
    return user
