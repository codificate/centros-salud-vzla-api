"""Firestore data-access layer for the 'centros' collection."""

from __future__ import annotations

from typing import Any, Final

from firebase_admin.firestore import Client as FirestoreClient

COLLECTION_NAME: Final[str] = "centros"


class CentrosRepository:
    """Encapsulates all Firestore reads/writes for health centers."""

    def __init__(self, client: FirestoreClient) -> None:
        self._client = client
        self._collection = client.collection(COLLECTION_NAME)

    def is_empty(self) -> bool:
        """Return True when the collection holds no documents."""
        docs = self._collection.limit(1).get()
        return len(docs) == 0

    def bulk_create(self, centros: list[dict[str, Any]]) -> int:
        """Batch-write centers using their 'id' as the document id."""
        batch = self._client.batch()
        for centro in centros:
            doc_ref = self._collection.document(str(centro["id"]))
            batch.set(doc_ref, centro)
        batch.commit()
        return len(centros)

    def list_all(self) -> list[dict[str, Any]]:
        """Return every center document in the collection."""
        return [doc.to_dict() for doc in self._collection.stream()]
