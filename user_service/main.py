from fastapi import FastAPI
from app.exceptions.exception_handlers import setup_exception_handlers
from app.api.router import router as user_router

app = FastAPI(root_path="/api/v1")

setup_exception_handlers(app)

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
