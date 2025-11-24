# app/schemas/robot_logs.py
# Schemas Pydantic para 'robot_logs'.

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RobotLogCreate(BaseModel):
    step_id: int
    function: Optional[str] = None
    filename: Optional[str] = None
    time_ms: Optional[float] = None
    docs: Optional[str] = None
    evidence: Optional[str] = None


class RobotLogUpdate(BaseModel):
    function: Optional[str] = None
    filename: Optional[str] = None
    status_id: Optional[int] = None
    time_ms: Optional[float] = None
    docs: Optional[str] = None
    evidence: Optional[str] = None


class RobotLogOut(BaseModel):
    id: int
    step_id: int
    function: Optional[str]
    filename: Optional[str]
    status_id: Optional[int]
    time_ms: Optional[float]
    docs: Optional[str]
    evidence: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
