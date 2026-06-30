"""HTTP controller for the 'insumos' resource."""

from __future__ import annotations

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException

from app.api.deps import InsumosServiceDep, UsuariosServiceDep
from app.api.middleware import get_user_uid
from app.schemas.insumo import InsumosCreateRequest, InsumosResponse
from app.services.insumos_service import InsumosService
from app.services.usuarios_service import UsuariosService

router = APIRouter(prefix="/insumos", tags=["insumos"])


@router.post("/", response_model=InsumosResponse, status_code=status.HTTP_201_CREATED)
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


@router.get("/by/{centro_id}", response_model=InsumosResponse)
def get_insumos_by_centro(
    centro_id: int,
    service: InsumosService = InsumosServiceDep,
) -> InsumosResponse:
    return service.list_by_centro(centro_id)
