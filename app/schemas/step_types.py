# app/schemas/step_types.py
# Schemas Pydantic para 'step_types'.

from pydantic import BaseModel
from typing import Optional


class StepTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None


class StepTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class StepTypeOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
