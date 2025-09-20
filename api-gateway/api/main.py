from fastapi import FastAPI

from api.exceptions.exception_handlers import setup_exception_handlers
from api.routers.v1 import router as v1_router

app = FastAPI(
    root_path="/api", title="API Gateway", version="0.0.1"
)

setup_exception_handlers(app)

app.include_router(v1_router)