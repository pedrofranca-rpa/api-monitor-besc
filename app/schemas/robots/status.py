# app/schemas/status_robot.py
# Schemas Pydantic para 'status_robot'.

from pydantic import BaseModel
from typing import Optional


class StatusRobotCreate(BaseModel):
    description: Optional[str] = None


class StatusRobotUpdate(BaseModel):
    description: Optional[str] = None


class StatusRobotOut(BaseModel):
    id: int
    description: Optional[str]

    class Config:
        from_attributes = True
