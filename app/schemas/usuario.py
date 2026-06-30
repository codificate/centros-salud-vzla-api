"""Pydantic schemas for the 'usuarios' resource."""

from __future__ import annotations

from pydantic import BaseModel

from app.schemas.centro import Centro


class SignUpRequest(BaseModel):
    centro_id: int
    mpps: int


class UserEntity(BaseModel):
    user_uid: str
    mpps: int
    centros: list[int]


class UserResponse(BaseModel):
    nombre: str
    mpps: int
    centros: list[Centro]
