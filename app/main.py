from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.main import api_router
from app.api.middleware import VerifyTokenMiddleware
from app.core.config import settings
from app.core.firebase import get_firestore, shutdown as firebase_shutdown
from app.repositories.centros_repository import CentrosRepository
from app.repositories.insumos_repository import InsumosRepository
from app.repositories.usuarios_repository import UsuariosRepository
from app.services.centros_service import CentrosService
from app.services.insumos_service import InsumosService
from app.services.usuarios_service import UsuariosService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Firebase, seed 'centros' if empty, tear down on shutdown."""
    client = get_firestore()
    app.state.firestore = client

    centros_repository = CentrosRepository(client)
    centros_service = CentrosService(centros_repository)
    app.state.centros_service = centros_service
    centros_service.seed_if_empty()

    app.state.usuarios_service = UsuariosService(
        UsuariosRepository(client), centros_repository
    )
    app.state.insumos_service = InsumosService(InsumosRepository(client))

    try:
        yield
    finally:
        firebase_shutdown()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(VerifyTokenMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=5001, reload=True)
