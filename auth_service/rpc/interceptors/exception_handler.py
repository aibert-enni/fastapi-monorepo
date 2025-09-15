import json
import logging
import grpc
from fastapi import status
from pydantic import ValidationError as PydanticValidationError

from app.exceptions.custom_exceptions import APIError

logger = logging.getLogger(__name__)

class ErrorInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        handler = await continuation(handler_call_details)

        if handler is None:
            return None

        # Для unary-unary методов
        if handler.unary_unary:
            async def error_handler(request, context):
                try:
                    return await handler.unary_unary(request, context) # type: ignore
                except APIError as e:
                    logger.error(e)
                    details = {
                        "http_code": e.http_code,
                        "error": {
                            "message": e.message
                        }
                    }
                    details_json = json.dumps(details, ensure_ascii=False)
                    context.set_details(details_json)
                    context.set_code(e.grpc_code)
                    return None
                except PydanticValidationError as e:
                    logger.error(e)
                    details = {
                        "http_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "error": {
                            "message": "Invalid request data",
                            "errors": e.errors()
                        }
                    }
                    details_json = json.dumps(details, ensure_ascii=False)
                    context.set_details(details_json)
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    return None
                except Exception as e:
                    logger.error(e)
                    context.set_details("Internal server error")
                    context.set_code(grpc.StatusCode.INTERNAL)
                    return None

            return grpc.unary_unary_rpc_method_handler(
                error_handler,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        # Для unary-stream, stream-unary, stream-stream можно аналогично добавить
        return handler
