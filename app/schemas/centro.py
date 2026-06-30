"""Pydantic schemas for health center (centro) documents."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Geolocalizacion(BaseModel):
    latitud: float
    longitud: float


class Centro(BaseModel):
    id: int
    nombre: str
    tipo: str
    direccion: str
    geolocalizacion: Geolocalizacion
    telefono: str | None = Field(default=None)
