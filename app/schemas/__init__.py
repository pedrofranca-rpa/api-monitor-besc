# app/schemas/__init__.py
# Importa todos os schemas para facilitar.

from .bots import BotCreate, BotUpdate, BotOut
from .environments import EnvironmentCreate, EnvironmentUpdate, EnvironmentOut
from .robots.status import StatusRobotCreate, StatusRobotUpdate, StatusRobotOut
from .step_types import StepTypeCreate, StepTypeUpdate, StepTypeOut
from .robots.runs import RobotRunCreate, RobotRunUpdate, RobotRunOut
from .robots.steps import RobotStepCreate, RobotStepUpdate, RobotStepOut
from .robots.logs import RobotLogCreate, RobotLogUpdate, RobotLogOut
from .robots.errors import RobotErrorCreate, RobotErrorUpdate, RobotErrorOut
