"""Business logic for the 'usuarios' resource."""

from __future__ import annotations

from app.repositories.centros_repository import CentrosRepository
from app.repositories.usuarios_repository import UsuariosRepository
from app.schemas.centro import Centro
from app.schemas.usuario import SignUpRequest, UserEntity, UserResponse


class UsuariosService:
    """Coordinates user persistence and response composition."""

    def __init__(
        self,
        repository: UsuariosRepository,
        centros_repository: CentrosRepository,
    ) -> None:
        self._repository = repository
        self._centros_repository = centros_repository

    def exists(self, user_uid: str) -> bool:
        """Return True when a user already exists for the given uid."""
        return self._repository.get_by_uid(user_uid) is not None

    def sign_up(
        self, user_uid: str, nombre: str, payload: SignUpRequest
    ) -> UserResponse:
        """Create a user and return it with resolved centers."""
        entity = UserEntity(
            user_uid=user_uid,
            mpps=payload.mpps,
            centros=[payload.centro_id],
        )
        self._repository.create(entity.model_dump())

        centros = [
            Centro.model_validate(doc)
            for doc in self._centros_repository.get_by_ids(entity.centros)
        ]
        return UserResponse(nombre=nombre, mpps=entity.mpps, centros=centros)
