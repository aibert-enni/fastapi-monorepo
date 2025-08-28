from fastapi import APIRouter

from app.schemas.user import UserCreateS, UserBaseS
from app.core.dependencies import UserServiceDep

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=UserBaseS)
async def create_user(user: UserCreateS, user_service: UserServiceDep):
    user = await user_service.create_user(user)
    return user
