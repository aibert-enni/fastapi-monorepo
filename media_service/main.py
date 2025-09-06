from fastapi import FastAPI

from app.api.v1 import router as v1_router
from app.exceptions.exception_handlers import setup_exception_handlers

app = FastAPI(root_path="/api", title="User Service", version="0.0.1")

setup_exception_handlers(app)

app.include_router(v1_router)


@app.get("/health", tags=["service"])
async def health():
    return {"status": "ok"}
