"""Authentication middleware verifying Firebase ID tokens."""

from __future__ import annotations

from firebase_admin import auth
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import settings
from app.core.firebase import get_app


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
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"},
            )

        try:
            decoded_token = auth.verify_id_token(token, app=get_app())
        except Exception:
            return JSONResponse(
                status_code=401, content={"detail": "Invalid or expired token"}
            )

        request.state.user = decoded_token
        return await call_next(request)


def get_user_uid(request: Request) -> str:
    """Return the authenticated user's uid from the decoded token."""
    return request.state.user["uid"]
