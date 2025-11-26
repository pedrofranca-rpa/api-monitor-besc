# app/schemas/robot_errors.py
# Schemas Pydantic para 'robot_errors'.

from pydantic import BaseModel
from typing import Optional


class RobotErrorCreate(BaseModel):
    step_id: int
    function: Optional[str] = None
    class_excpt: Optional[str] = None
    traceback: Optional[str] = None


class RobotErrorUpdate(BaseModel):
    function: Optional[str] = None
    class_excpt: Optional[str] = None
    traceback: Optional[str] = None


class RobotErrorOut(BaseModel):
    id: int
    step_id: int
    function: Optional[str]
    class_excpt: Optional[str]
    traceback: Optional[str]

    class Config:
        from_attributes = True
