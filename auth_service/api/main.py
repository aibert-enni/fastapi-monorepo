from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.exceptions.exception_handlers import setup_exception_handlers
from api.router.v1 import router as v1_router
from app.core.settings import settings
from app.services.brokers.broker_manager import get_broker_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.rabbit.ENABLE:
        await get_broker_manager().initalize("rabbit")
    else:
        await get_broker_manager().initalize("dummy")
    yield
    await get_broker_manager().shutdown()


app = FastAPI(
    root_path="/api", title="Auth Service", version="0.0.1", lifespan=lifespan
)

setup_exception_handlers(app)

app.include_router(v1_router)


@app.get("/health", tags=["service"])
async def health():
    return {"status": "ok"}
