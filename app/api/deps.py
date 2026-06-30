from fastapi import Depends, Request, Security
from fastapi.security import HTTPBearer
from firebase_admin.firestore import Client as FirestoreClient

from app.services.centros_service import CentrosService
from app.services.insumos_service import InsumosService
from app.services.usuarios_service import UsuariosService

# Bearer scheme for OpenAPI docs only; the actual verification is performed
# by VerifyTokenMiddleware. auto_error=False avoids a duplicate 403 here.
bearer_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="FirebaseBearer",
    description="Firebase ID token. Send as 'Authorization: Bearer <token>'.",
)
BearerSecurity = Security(bearer_scheme)


def get_firestore_client(request: Request) -> FirestoreClient:
    """Return the Firestore client attached to the application state."""
    return request.app.state.firestore


def get_centros_service(request: Request) -> CentrosService:
    """Return the CentrosService attached to the application state."""
    return request.app.state.centros_service


def get_usuarios_service(request: Request) -> UsuariosService:
    """Return the UsuariosService attached to the application state."""
    return request.app.state.usuarios_service


def get_insumos_service(request: Request) -> InsumosService:
    """Return the InsumosService attached to the application state."""
    return request.app.state.insumos_service


FirestoreDep = Depends(get_firestore_client)
CentrosServiceDep = Depends(get_centros_service)
UsuariosServiceDep = Depends(get_usuarios_service)
InsumosServiceDep = Depends(get_insumos_service)
