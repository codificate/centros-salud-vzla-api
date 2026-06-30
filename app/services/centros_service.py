"""Business logic for seeding and reading health centers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

from app.repositories.centros_repository import CentrosRepository
from app.schemas.centro import Centro

_SEED_FILE: Final[Path] = Path(__file__).resolve().parent.parent / "core" / "centros.json"


class CentrosService:
    """Coordinates repository access and seed-data loading."""

    def __init__(self, repository: CentrosRepository) -> None:
        self._repository = repository

    def seed_if_empty(self) -> int:
        """Bulk-load centros.json when the collection is empty.

        Returns the number of documents inserted (0 when already seeded).
        """
        if not self._repository.is_empty():
            return 0
        centros = self._load_seed_data()
        return self._repository.bulk_create(centros)

    def list_centros(self) -> list[Centro]:
        """Return all centers as validated schemas."""
        return [Centro.model_validate(doc) for doc in self._repository.list_all()]

    @staticmethod
    def _load_seed_data() -> list[dict[str, Any]]:
        with _SEED_FILE.open(encoding="utf-8") as fp:
            data = json.load(fp)
        # Validate before writing so malformed seed data fails fast.
        return [Centro.model_validate(item).model_dump() for item in data]
