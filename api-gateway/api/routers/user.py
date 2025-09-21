from fastapi import APIRouter
import grpc

from app.core.settings import settings
from api.dependencies.current_user import GetCurrentUserDep
from proto.user import user_pb2, user_pb2_grpc
from app.schemas.user import UserS
from api.schemas.user import UserUpdateRequestS

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
async def create_user(schema: UserS) -> UserS:
    async with grpc.aio.insecure_channel(settings.grpc.user_url) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.CreateUserRequest(id=str(schema.id), first_name=schema.first_name, last_name=schema.last_name)
        response = await stub.CreateUser(request)
    return UserS(id=response.id, first_name=response.first_name, last_name=response.last_name)

@router.put("/me")
async def update_current_user(schema: UserUpdateRequestS, current_user: GetCurrentUserDep) -> UserS:
    async with grpc.aio.insecure_channel(settings.grpc.user_url) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.UpdateUserRequest(id=str(current_user.id), first_name=schema.first_name, last_name=schema.last_name)
        response = await stub.UpdateUser(request)
    return UserS(id=response.id, first_name=response.first_name, last_name=response.last_name)