from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .custom_exceptions import APIError, DatabaseError


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DatabaseError)
    async def database_exception_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error,
                "message": exc.message,
            },
        )

    @app.exception_handler(APIError)
    async def api_exception_handler(request: Request, exc: APIError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error,
                "message": exc.message,
            },
        )
