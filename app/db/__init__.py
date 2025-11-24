# app/db/__init__.py
from .base import Base

# app/db/base.py

from app.db import Base

# IMPORTAR TODAS MODELS EXPLICITAMENTE
from app.models.bots import Bot
from app.models.user import User
from app.models.environments import Environment
from app.models.step_types import StepType
from app.models.robots.status import StatusRobot
from app.models.robots.runs import RobotRun
from app.models.robots.steps import RobotStep
from app.models.robots.logs import RobotLog
from app.models.robots.errors import RobotError


__all__ = ["Base"]
