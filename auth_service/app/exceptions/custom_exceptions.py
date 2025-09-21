from typing import Optional

from fastapi import status
from grpc import StatusCode


class AppError(Exception):
    http_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    grpc_code = StatusCode.INTERNAL

    def __init__(
        self,
        message: str,
        http_code: Optional[int]= None,
        grpc_code:  Optional[StatusCode] = None
    ):
        self.message = message
        if http_code is not None:
            self.http_code = http_code
        if grpc_code is not None:
            self.grpc_code = grpc_code


class APIError(AppError):
    pass

class IntegrityError(APIError):
    grpc_code = StatusCode.INVALID_ARGUMENT
    http_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str = "Data validation error"):
        super().__init__(message)


class NotFoundError(APIError):
    grpc_code = StatusCode.NOT_FOUND
    http_code=status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)

class CredentialError(APIError):
    grpc_code = StatusCode.UNAUTHENTICATED
    http_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        message: str = "Invalid credentials",
    ):
        super().__init__(message)


class AuthorizationError(APIError):
    grpc_code = StatusCode.PERMISSION_DENIED
    http_code = status.HTTP_403_FORBIDDEN

    def __init__(
        self,
        message: str = "You don't have permission to access this resource."
    ):
        super().__init__(message)


class ValidationError(APIError):
    grpc_code = StatusCode.INVALID_ARGUMENT
    http_code = status.HTTP_422_UNPROCESSABLE_ENTITY

class BadRequestError(APIError):
    grpc_code = StatusCode.INVALID_ARGUMENT
    http_code = status.HTTP_400_BAD_REQUEST

class ServiceUnavailableError(APIError):
    grpc_code = StatusCode.UNAVAILABLE
    http_code = status.HTTP_503_SERVICE_UNAVAILABLE

    def __init__(
        self,
        message: str = "Service unavailable",
    ):
        super().__init__(message)
