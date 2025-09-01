from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import router as v1_router
from app.exceptions.exception_handlers import setup_exception_handlers
from app.services.brokers.rabbit.main import rabbit_broker_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_broker_service.start()
    yield
    await rabbit_broker_service.stope()


app = FastAPI(
    root_path="/api", title="Auth Service", version="0.0.1", lifespan=lifespan
)

setup_exception_handlers(app)

app.include_router(v1_router)


@app.get("/health", tags=["service"])
async def health():
    return {"status": "ok"}
