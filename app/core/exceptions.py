from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or self._default_error_code()

    def _default_error_code(self) -> str:
        return "API_ERROR"


class AuthenticationError(BaseAPIException):
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_ERROR",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredError(BaseAPIException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="TOKEN_EXPIRED",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenValidationError(BaseAPIException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="TOKEN_INVALID",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenError(BaseAPIException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN",
        )


class NotFoundError(BaseAPIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND",
        )


class ValidationError(BaseAPIException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
        )


class RateLimitError(BaseAPIException):
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class InternalServerError(BaseAPIException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="INTERNAL_ERROR",
        )


class DatabaseError(BaseAPIException):
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR",
        )


class DatabaseConnectionError(BaseAPIException):
    def __init__(self, detail: str = "Failed to connect to database"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code="DATABASE_CONNECTION_ERROR",
        )


class DatabaseIntegrityError(BaseAPIException):
    def __init__(self, detail: str = "Database integrity constraint violated"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="DATABASE_INTEGRITY_ERROR",
        )


def create_error_response(
    status_code: int,
    detail: str,
    error_code: str,
    path: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "error": {
            "code": error_code,
            "message": detail,
            "status": status_code,
            "path": path,
        }
    }


async def base_api_exception_handler(
    request: Request, exc: BaseAPIException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            detail=exc.detail,
            error_code=exc.error_code,
            path=str(request.url.path),
        ),
        headers=exc.headers,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            detail=exc.detail,
            error_code="HTTP_ERROR",
            path=str(request.url.path),
        ),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
            error_code="INTERNAL_ERROR",
            path=str(request.url.path),
        ),
    )
