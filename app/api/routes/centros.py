"""HTTP controller for the 'centros' resource."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import CentrosServiceDep
from app.schemas.centro import Centro
from app.services.centros_service import CentrosService

router = APIRouter(prefix="/centros", tags=["centros"])


@router.get(
    "/",
    response_model=list[Centro],
    summary="List health centers",
    description="Return every health center. Public endpoint, no token required.",
    response_description="The list of health centers.",
)
def list_centros(service: CentrosService = CentrosServiceDep) -> list[Centro]:
    return service.list_centros()
