# app/schemas/bots.py
# Schemas Pydantic para 'bots'.

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BotCreate(BaseModel):
    name: str
    description: Optional[str] = None


class BotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class BotOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
