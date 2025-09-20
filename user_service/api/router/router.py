from uuid import UUID

from fastapi import APIRouter

from api.dependencies.services import UserServiceDep
from app.schemas.user import UserBaseS, UserS, UserUpdateS

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/update", response_model=UserS)
async def update_user(user_id: UUID, schema: UserBaseS, user_service: UserServiceDep):
    create_schema = UserUpdateS(id=user_id, **schema.model_dump())
    user = await user_service.update_user(create_schema)
    return user
