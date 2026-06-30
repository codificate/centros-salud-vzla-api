from fastapi import APIRouter

from app.api.routes import centros, items, usuarios

api_router = APIRouter()
api_router.include_router(items.router)
api_router.include_router(centros.router)
api_router.include_router(usuarios.router)
