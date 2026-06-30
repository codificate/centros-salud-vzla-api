"""HTTP controller for the 'insumos' resource."""

from __future__ import annotations

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException

from app.api.deps import BearerSecurity, InsumosServiceDep, UsuariosServiceDep
from app.api.middleware import get_user_uid
from app.schemas.insumo import InsumosCreateRequest, InsumosResponse
from app.services.insumos_service import InsumosService
from app.services.usuarios_service import UsuariosService

router = APIRouter(prefix="/insumos", tags=["insumos"])


@router.post(
    "/",
    response_model=InsumosResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[BearerSecurity],
    summary="Register supplies for a centro",
    description=(
        "Store supplies in the centro's 'insumos' subcollection. The "
        "authenticated user must be assigned to the target centro."
    ),
    response_description="The created supplies.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid token"},
        status.HTTP_403_FORBIDDEN: {"description": "User not assigned to this centro"},
    },
)
def create_insumos(
    request: Request,
    payload: InsumosCreateRequest,
    service: InsumosService = InsumosServiceDep,
    usuarios_service: UsuariosService = UsuariosServiceDep,
) -> InsumosResponse:
    user_uid = get_user_uid(request)

    if not usuarios_service.has_centro(user_uid, payload.centro):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not assigned to this centro",
        )

    return service.create(user_uid, payload)


@router.get(
    "/by/{centro_id}",
    response_model=InsumosResponse,
    dependencies=[BearerSecurity],
    summary="List supplies by centro",
    description="Return supplies for the given centro, sorted by creation date (newest first).",
    response_description="The centro's supplies.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid token"},
    },
)
def get_insumos_by_centro(
    centro_id: int,
    service: InsumosService = InsumosServiceDep,
) -> InsumosResponse:
    return service.list_by_centro(centro_id)
