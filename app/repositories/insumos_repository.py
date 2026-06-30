"""Firestore data-access layer for the 'insumos' subcollection.

Each centro document holds its own 'insumos' subcollection:
    centros/{centro_id}/insumos/{auto_id}
"""

from __future__ import annotations

from typing import Any, Final

from firebase_admin.firestore import Client as FirestoreClient
from google.cloud.firestore_v1 import Query

CENTROS_COLLECTION: Final[str] = "centros"
INSUMOS_SUBCOLLECTION: Final[str] = "insumos"
CREATED_AT_FIELD: Final[str] = "create_at"


class InsumosRepository:
    """Encapsulates Firestore reads/writes for centro supplies."""

    def __init__(self, client: FirestoreClient) -> None:
        self._client = client
        self._centros = client.collection(CENTROS_COLLECTION)

    def _subcollection(self, centro_id: int):
        return self._centros.document(str(centro_id)).collection(INSUMOS_SUBCOLLECTION)

    def bulk_create(self, centro_id: int, insumos: list[dict[str, Any]]) -> int:
        """Batch-write supplies into the centro's 'insumos' subcollection."""
        batch = self._client.batch()
        subcollection = self._subcollection(centro_id)
        for insumo in insumos:
            batch.set(subcollection.document(), insumo)
        batch.commit()
        return len(insumos)

    def list_by_centro(self, centro_id: int) -> list[dict[str, Any]]:
        """Return every supply under the given centro, newest first."""
        query = self._subcollection(centro_id).order_by(
            CREATED_AT_FIELD, direction=Query.DESCENDING
        )
        return [doc.to_dict() for doc in query.stream()]
