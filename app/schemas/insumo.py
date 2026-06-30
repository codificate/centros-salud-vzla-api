"""Pydantic schemas for the 'insumos' subcollection."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class InsumoItem(BaseModel):
    cantidad: int
    descripcion: str


class InsumosCreateRequest(BaseModel):
    centro: int
    insumos: list[InsumoItem]


class InsumoEntity(BaseModel):
    user_uid: str
    centro: int
    cantidad: int
    descripcion: str
    create_at: datetime


class InsumoResponseItem(BaseModel):
    cantidad: int
    descripcion: str
    create_at: datetime


class InsumosResponse(BaseModel):
    insumos: list[InsumoResponseItem]
