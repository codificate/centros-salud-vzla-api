"""Firestore data-access layer for the 'usuarios' collection."""

from __future__ import annotations

from typing import Any, Final

from firebase_admin.firestore import Client as FirestoreClient

COLLECTION_NAME: Final[str] = "usuarios"


class UsuariosRepository:
    """Encapsulates all Firestore reads/writes for users."""

    def __init__(self, client: FirestoreClient) -> None:
        self._collection = client.collection(COLLECTION_NAME)

    def get_by_uid(self, user_uid: str) -> dict[str, Any] | None:
        """Return the user document for the given uid, or None."""
        snapshot = self._collection.document(user_uid).get()
        return snapshot.to_dict() if snapshot.exists else None

    def create(self, user: dict[str, Any]) -> None:
        """Persist a user using its 'user_uid' as the document id."""
        self._collection.document(user["user_uid"]).set(user)
