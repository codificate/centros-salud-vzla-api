"""Authentication middleware verifying Firebase ID tokens."""

from __future__ import annotations

from enum import StrEnum

from fastapi import status
from firebase_admin import auth
from firebase_admin import exceptions as firebase_exceptions
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import settings
from app.core.firebase import get_app


class VerificationErrorType(StrEnum):
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED_TOKEN = "EXPIRED_TOKEN"
    REVOKED_TOKEN = "REVOKED_TOKEN"
    SERVER_ERROR = "SERVER_ERROR"

def _unauthorized(detail: str, error_type: VerificationErrorType) -> JSONResponse:
    """Build a 401 response with a Bearer challenge."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": detail, "error_type": error_type},
        headers={"WWW-Authenticate": "Bearer"},
    )


def _is_public(request: Request) -> bool:
    """Public routes that bypass token verification."""
    path = request.url.path
    if request.method == "OPTIONS":
        return True
    if path in {"/", "/docs", "/redoc", "/openapi.json", "/favicon.ico"}:
        return True
    # Public: GET /api/v1/centros and its sub-paths.
    centros_prefix = f"{settings.API_V1_STR}/centros"
    if request.method == "GET" and path.startswith(centros_prefix):
        return True
    return False


class VerifyTokenMiddleware(BaseHTTPMiddleware):
    """Verify the Firebase ID token and attach the decoded claims."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if _is_public(request):
            return await call_next(request)

        header = request.headers.get("Authorization", "")
        scheme, _, token = header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing or invalid Authorization header",
                    "error_type": VerificationErrorType.INVALID_TOKEN,
                },
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            decoded_token = auth.verify_id_token(token, app=get_app())
        except auth.ExpiredIdTokenError:
            return _unauthorized("Expired token", VerificationErrorType.EXPIRED_TOKEN)
        except auth.RevokedIdTokenError:
            return _unauthorized("Revoked token", VerificationErrorType.REVOKED_TOKEN)
        except auth.InvalidIdTokenError:
            return _unauthorized("Invalid token", VerificationErrorType.INVALID_TOKEN)
        except ValueError:
            return _unauthorized("Invalid token", VerificationErrorType.INVALID_TOKEN)
        except firebase_exceptions.FirebaseError:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "detail": "Authentication service unavailable",
                    "error_type": VerificationErrorType.SERVER_ERROR,
                },
            )

        request.state.user = decoded_token
        return await call_next(request)


def get_user_uid(request: Request) -> str:
    """Return the authenticated user's uid from the decoded token."""
    return request.state.user["uid"]
