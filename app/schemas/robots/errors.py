# app/schemas/robot_errors.py
# Schemas Pydantic para 'robot_errors'.

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RobotErrorCreate(BaseModel):
    log_id: int
    function: Optional[str] = None
    class_excpt: Optional[str] = None
    traceback: Optional[str] = None
    created_at: datetime


class RobotErrorUpdate(BaseModel):
    function: Optional[str] = None
    class_excpt: Optional[str] = None
    traceback: Optional[str] = None


class RobotErrorOut(BaseModel):
    id: int
    log_id: int
    function: Optional[str]
    class_excpt: Optional[str]
    traceback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
