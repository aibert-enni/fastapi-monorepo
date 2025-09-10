from fastapi import status


class DatabaseError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.message = message
        self.status_code = status_code


class IntegrityError(DatabaseError):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)


class NotFoundError(DatabaseError):
    def __init__(
        self,
        message,
        status_code=status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message, status_code)


class APIError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


class CredentialError(APIError):
    def __init__(
        self,
        message: str = "Invalid credentials",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)


class AuthorizationError(APIError):
    def __init__(
        self,
        message: str = "You don't have permission to access this resource.",
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        super().__init__(message, status_code)


class ValidationError(APIError):
    def __init__(
        self, message: str, status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    ):
        super().__init__(message, status_code)


class BadRequestError(APIError):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)


class ServiceUnavailableError(APIError):
    def __init__(
        self,
        message: str = "Service unavailable, please try later",
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
    ):
        super().__init__(message, status_code)


class UnsupportedMediaTypeError(APIError):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    ):
        super().__init__(message, status_code)
