from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI

from app.core.setup import setup    
from api.exceptions.exception_handlers import setup_exception_handlers
from api.routers.v1 import router as v1_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup()
    yield

app = FastAPI(
    root_path="/api", title="API Gateway", version="0.0.1", lifespan=lifespan
)

setup_exception_handlers(app)

app.include_router(v1_router)