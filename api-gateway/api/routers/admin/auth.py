from uuid import UUID

from api.dependencies.current_user import GetHttpBearerDep, get_current_superuser
from api.dependencies.grpc import get_auth_stub
from api.schemas.auth import (
    AuthS,
    CreateUserByAdminRequest,
    CreateUserByAdminResponse,
    DeleteUserByAdminResponse,
    UpdateUserByAdminRequest,
    UpdateUserByAdminResponse,
)
from fastapi import APIRouter, Depends
from proto.auth import auth_pb2

router = APIRouter(prefix="/auth", tags=["admin-auth"], dependencies=[Depends(get_current_superuser)])

@router.post("/")
async def create_user(schema: CreateUserByAdminRequest, bearer_token: GetHttpBearerDep) -> CreateUserByAdminResponse:
    async with get_auth_stub() as stub:
        request = auth_pb2.CreateUserByAdminRequest(access_token=bearer_token.credentials, username=schema.username, email=schema.email, password=schema.password, is_active=schema.is_active, is_superuser=schema.is_superuser)
        response = await stub.CreateUserByAdmin(request)
    return CreateUserByAdminResponse(id=response.id, username=response.username, email=response.email, is_active=response.is_active, is_superuser=response.is_superuser)

@router.put("/{user_id}")
async def update_user(user_id: UUID, schema: UpdateUserByAdminRequest, bearer_token: GetHttpBearerDep) -> UpdateUserByAdminResponse:
    async with get_auth_stub() as stub:
        request = auth_pb2.UpdateUserByAdminRequest(access_token=bearer_token.credentials, id=str(user_id), username=schema.username, password=schema.password, email=schema.email, is_active=schema.is_active, is_superuser=schema.is_superuser)
        response = await stub.UpdateUserByAdmin(request)
    return UpdateUserByAdminResponse(id=response.id, username=response.username, email=response.email, is_active=response.is_active, is_superuser=response.is_superuser)

@router.delete("/{user_id}")
async def delete_user(user_id: UUID, bearer_token: GetHttpBearerDep) -> DeleteUserByAdminResponse:
    async with get_auth_stub() as stub:
        request = auth_pb2.DeleteUserByAdminRequest(access_token=bearer_token.credentials, id=str(user_id))
        response = await stub.DeleteUserByAdmin(request)
    return DeleteUserByAdminResponse(id=response.id, is_deleted=response.is_deleted)

@router.get("/")
async def get_all_users(bearer_token: GetHttpBearerDep) -> list[AuthS]:
    async with get_auth_stub() as stub:
        request = auth_pb2.GetAllUsersByAdminRequest(access_token=bearer_token.credentials)
        response = await stub.GetAllUsersByAdmin(request)
    return [AuthS(id=user.id, username=user.username, email=user.email, is_active=user.is_active, is_superuser=user.is_superuser) for user in response.users]