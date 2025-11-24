# app/schemas/robot_steps.py
# Schemas Pydantic para 'robot_steps'.

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.robots.logs import RobotLogOut


class RobotStepCreate(BaseModel):
    run_id: int
    step_type_id: int
    ended_at: Optional[datetime] = None


class RobotStepUpdate(BaseModel):
    status_id: Optional[int] = None
    ended_at: Optional[datetime] = None


class RobotStepOut(BaseModel):
    id: int
    run_id: int
    step_type_id: int
    status_id: int
    ended_at: Optional[datetime]

    class Config:
        from_attributes = True
