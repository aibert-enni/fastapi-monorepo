from api.dependencies.current_user import (
    GetCurrentUserByRefreshDep,
    GetCurrentUserDep,
    get_current_user_by_refresh,
)
from api.dependencies.services import AuthServiceDep
from fastapi import APIRouter, Depends, Response

from app.schemas.auth import (
    AuthBaseS,
    AuthCreateS,
    AuthLoginS,
    AuthRegisterResponseS,
    AuthRegisterS,
)
from app.schemas.jwt_token import AccessTokenS
from app.utils.jwt import create_access_token

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
    auth_schema =  await auth_service.create_auth(create_schema)
    response_schema = AuthRegisterResponseS.model_validate(auth_schema)
    return response_schema


@router.post("/login", status_code=200)
async def login_user(
    schema: AuthLoginS, response: Response, auth_service: AuthServiceDep
) -> AccessTokenS:
    tokens = await auth_service.login_user(schema)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return AccessTokenS(access_token=tokens.access_token)


@router.post("/refresh", status_code=200)
async def refresh_access_token(
    current_user: GetCurrentUserByRefreshDep,
) -> AccessTokenS:
    access_token = create_access_token({"sub": current_user.username})

    return AccessTokenS(access_token=access_token)


@router.get("/me", status_code=200)
async def get_user_me(
    current_user: GetCurrentUserDep,
) -> AuthBaseS:
    return current_user


@router.post(
    "/logout", status_code=200, dependencies=[Depends(get_current_user_by_refresh)]
)
async def logout_user(response: Response) -> dict:
    response.delete_cookie(key="refresh_token", httponly=True, secure=True)
    return {"message": "Logget out"}
