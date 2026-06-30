from datetime import datetime, timezone

from fastapi import Depends, Request
from firebase_admin.firestore import Client as FirestoreClient

from app.services.centros_service import CentrosService


def get_timestamp() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def get_firestore_client(request: Request) -> FirestoreClient:
    """Return the Firestore client attached to the application state."""
    return request.app.state.firestore


def get_centros_service(request: Request) -> CentrosService:
    """Return the CentrosService attached to the application state."""
    return request.app.state.centros_service


FirestoreDep = Depends(get_firestore_client)
CentrosServiceDep = Depends(get_centros_service)
