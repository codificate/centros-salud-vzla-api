from fastapi import APIRouter

from app.api.routes import centros, insumos, usuarios

api_router = APIRouter()
api_router.include_router(centros.router)
api_router.include_router(usuarios.router)
api_router.include_router(insumos.router)
