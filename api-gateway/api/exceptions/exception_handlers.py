import json

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from grpc import StatusCode
from grpc.aio import AioRpcError

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
    
    @app.exception_handler(AioRpcError)
    async def grpc_exception_handler(request: Request, exc: AioRpcError) -> JSONResponse:
        if exc.code() == StatusCode.UNAVAILABLE:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "message": "Service unavailable, try again later",
                }
            )

        details = exc.details()
        try:
            json_response = json.loads(details) if details else {}
            if json_response is str:
                json_response = {}
        except Exception:
            json_response = {}
        http_code = json_response.get("http_code", 500)
        http_code = int(http_code)
        content = json_response.get("error", {"message": details})
        return JSONResponse(
            status_code=http_code,
            content=content,
        )