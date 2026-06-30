"""Business logic for the 'insumos' subcollection."""

from __future__ import annotations

from datetime import datetime, timezone

from app.repositories.insumos_repository import InsumosRepository
from app.schemas.insumo import (
    InsumoEntity,
    InsumoResponseItem,
    InsumosCreateRequest,
    InsumosResponse,
)


class InsumosService:
    """Coordinates supply persistence and response composition."""

    def __init__(self, repository: InsumosRepository) -> None:
        self._repository = repository

    def create(self, user_uid: str, payload: InsumosCreateRequest) -> InsumosResponse:
        """Persist supplies for a centro and return them."""
        created_at = datetime.now(timezone.utc)
        entities = [
            InsumoEntity(
                user_uid=user_uid,
                centro=payload.centro,
                cantidad=item.cantidad,
                descripcion=item.descripcion,
                create_at=created_at,
            )
            for item in payload.insumos
        ]
        self._repository.bulk_create(
            payload.centro, [e.model_dump() for e in entities]
        )
        return self._to_response(entities)

    def list_by_centro(self, centro_id: int) -> InsumosResponse:
        """Return every supply stored under the given centro."""
        entities = [
            InsumoEntity.model_validate(doc)
            for doc in self._repository.list_by_centro(centro_id)
        ]
        return self._to_response(entities)

    @staticmethod
    def _to_response(entities: list[InsumoEntity]) -> InsumosResponse:
        return InsumosResponse(
            insumos=[
                InsumoResponseItem(
                    cantidad=e.cantidad,
                    descripcion=e.descripcion,
                    create_at=e.create_at,
                )
                for e in entities
            ]
        )
