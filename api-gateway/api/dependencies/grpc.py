from contextlib import asynccontextmanager
from typing import AsyncIterator

import grpc
from proto.auth import auth_pb2_grpc

from app.core.settings import settings


@asynccontextmanager
async def get_auth_stub() -> AsyncIterator[auth_pb2_grpc.AuthStub]:
    async with grpc.aio.insecure_channel(settings.grpc.auth_url) as channel:
        stub = auth_pb2_grpc.AuthStub(channel)
        yield stub