# app/schemas/robot_runs.py
# Schemas Pydantic para 'robot_runs'.

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RobotRunCreate(BaseModel):
    bot_id: int
    env_id: int
    host: str
    total_process: Optional[int] = None


class RobotRunUpdate(BaseModel):
    status_id: Optional[int] = None
    total_process: Optional[int] = None


class RobotRunOut(BaseModel):
    id: int
    bot_id: int
    created_at: datetime
    end_at: Optional[datetime]
    status_id: int
    total_process: Optional[int]
    env_id: int
    host: str

    class Config:
        from_attributes = True
