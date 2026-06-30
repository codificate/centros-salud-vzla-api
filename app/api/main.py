from fastapi import APIRouter

from app.api.routes import centros, items

api_router = APIRouter()
api_router.include_router(items.router)
api_router.include_router(centros.router)
