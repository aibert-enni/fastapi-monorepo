from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import UserServiceDep
from app.schemas.user import UserBaseS, UserCreateS, UserS

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/update", response_model=UserS)
async def update_user(user_id: UUID, schema: UserBaseS, user_service: UserServiceDep):
    create_schema = UserCreateS(id=user_id, **schema.model_dump())
    user = await user_service.update_user(create_schema)
    return user
