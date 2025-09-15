import logging
from fastapi import APIRouter, Request, Response, status
import grpc

from app.core.settings import settings
from app.schemas.auth import AuthRegisterRequestS, AuthRegisterResponseS, AuthLoginRequestS, AuthLoginResponseS, RefreshAccessTokenResponse, AuthMeResponse
from app.exceptions.custom_exceptions import CredentialError
from app.utils.jwt import decode_jwt
from api.dependencies.current_user import GetCurrentUserDep
from proto.auth import auth_pb2_grpc, auth_pb2

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(schema: AuthRegisterRequestS) -> AuthRegisterResponseS:
    async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        request = auth_pb2.AuthRegisterRequest(username=schema.username, email=schema.email, password=schema.password)
        
        response = await stub.RegisterUser(request)
    
    return AuthRegisterResponseS(id=response.id, username=response.username)

@router.post("/login")
async def user_login(schema: AuthLoginRequestS, response: Response) -> AuthLoginResponseS:
    async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        request = auth_pb2.AuthLoginRequest(username=schema.username, password=schema.password)

        rpc_response = await stub.LoginUser(request)
    
    response.set_cookie(
        key="refresh_token",
        value=rpc_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return AuthLoginResponseS(access_token=rpc_response.access_token)

@router.post("/refresh")
async def refresh_access_token(request: Request) -> RefreshAccessTokenResponse:
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise CredentialError
    try:
        payload = decode_jwt(refresh_token)
    except Exception:
        raise CredentialError
    
    async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        request = auth_pb2.RefreshAccessTokenRequest(payload=payload)

        response = await stub.RefreshAccessToken(request)

    return RefreshAccessTokenResponse(access_token=response.access_token)

@router.get("/me")
async def get_user_me(
    current_user: GetCurrentUserDep,
) -> AuthMeResponse:
    return AuthMeResponse(id=current_user.id, username=current_user.username)

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token", httponly=True, secure=True, samesite="lax")
    return {"result": "success"}