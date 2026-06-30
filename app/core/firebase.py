"""Firebase Admin SDK initialization.

Lazely initializes a single app instance per process and exposes
helper accessors for Firestore, Auth, and the bucket client.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Final

import firebase_admin
from firebase_admin import App, auth, credentials, firestore, storage
from firebase_admin.firestore import Client as FirestoreClient

from app.core.config import settings


_FIREBASE_APP_NAME: Final[str] = "centros-salud-vzla-api"


def _credentials_from_file() -> credentials.Certificate:
    """Load credentials from the local service account JSON file (dev)."""
    creds_path = settings.FIREBASE_CREDENTIALS_PATH
    if not creds_path:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS_PATH is not set for the dev environment"
        )
    path = Path(creds_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Firebase credentials not found: {path}")
    return credentials.Certificate(str(path))


def _credentials_from_env() -> credentials.Certificate:
    """Load credentials from the FIREBASE_CREDENTIALS env var (prod/vercel)."""
    raw = settings.FIREBASE_CREDENTIALS
    if not raw:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS env var is not set for the "
            f"'{settings.ENVIRONMENT}' environment"
        )
    try:
        service_account = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("FIREBASE_CREDENTIALS is not valid JSON") from exc
    return credentials.Certificate(service_account)


def _resolve_credentials() -> credentials.Certificate:
    """Pick the credentials source based on the ENVIRONMENT setting."""
    if settings.is_dev:
        return _credentials_from_file()
    return _credentials_from_env()


def _build_app() -> App:
    """Build a new Firebase app with credentials from file or env."""
    if firebase_admin._apps:
        return firebase_admin.get_app(_FIREBASE_APP_NAME)

    cred = _resolve_credentials()

    options: dict[str, str] = {}
    if settings.FIREBASE_STORAGE_BUCKET:
        options["storageBucket"] = settings.FIREBASE_STORAGE_BUCKET
    if settings.FIREBASE_PROJECT_ID:
        options["projectId"] = settings.FIREBASE_PROJECT_ID

    return firebase_admin.initialize_app(
        credential=cred,
        options=options or None,
        name=_FIREBASE_APP_NAME,
    )


def get_app() -> App:
    """Return the initialized Firebase app, building it on first call."""
    try:
        return firebase_admin.get_app(_FIREBASE_APP_NAME)
    except ValueError:
        return _build_app()


@lru_cache(maxsize=1)
def get_firestore() -> FirestoreClient:
    """Return a cached Firestore client bound to the default database."""
    return firestore.client(app=get_app())


def get_auth():
    """Return the Firebase Auth client."""
    return auth.Client(app=get_app())


def get_storage_bucket():
    """Return the default Cloud Storage bucket client."""
    return storage.bucket(app=get_app())


def shutdown() -> None:
    """Delete the Firebase app and clear the cache (for tests / shutdown)."""
    global FirestoreClient  # noqa: FPLW063
    try:
        firebase_admin.delete_app(_FIREBASE_APP_NAME)
    except ValueError:
        pass
    get_firestore.cache_clear()
