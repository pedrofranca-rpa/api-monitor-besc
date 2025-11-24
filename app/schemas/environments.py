# app/schemas/environments.py
# Schemas Pydantic para 'environments'.

from pydantic import BaseModel
from typing import Optional


class EnvironmentCreate(BaseModel):
    name: str
    description: Optional[str] = None


class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class EnvironmentOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
