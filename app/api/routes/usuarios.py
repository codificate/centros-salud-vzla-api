"""HTTP controller for the 'usuarios' resource."""

from __future__ import annotations

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException

from app.api.deps import UsuariosServiceDep
from app.api.middleware import get_user_uid
from app.schemas.usuario import SignUpRequest, UserResponse
from app.services.usuarios_service import UsuariosService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/sign-up", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(
    request: Request,
    payload: SignUpRequest,
    service: UsuariosService = UsuariosServiceDep,
) -> UserResponse:
    user_uid = get_user_uid(request)

    if service.exists(user_uid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    nombre = request.state.user.get("name", "")
    return service.sign_up(user_uid, nombre, payload)


@router.get("/sign-in", response_model=UserResponse)
def sign_in(
    request: Request,
    service: UsuariosService = UsuariosServiceDep,
) -> UserResponse:
    user_uid = get_user_uid(request)
    nombre = request.state.user.get("name", "")

    user = service.get_user(user_uid, nombre)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
