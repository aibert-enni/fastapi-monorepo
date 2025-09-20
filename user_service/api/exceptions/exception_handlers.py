from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import APIError


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(APIError)
    async def api_exception_handler(request: Request, exc: APIError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_code,
            content={
                "message": exc.message,
            },
        )
