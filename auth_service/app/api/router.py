from fastapi import APIRouter

from app.core.dependencies import AuthServiceDep
from app.schemas.auth import AuthCreateS, AuthRegisterResponseS, AuthRegisterS

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=201)
async def register_user(
    schema: AuthRegisterS, auth_service: AuthServiceDep
) -> AuthRegisterResponseS:
    create_schema = AuthCreateS(
        **schema.model_dump(), is_active=True, is_superuser=False
    )
    return await auth_service.create_auth(create_schema)
