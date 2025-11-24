# app/routers/__init__.py
# Importa todos os routers.

from .bots import router as bots_router
from .environments import router as environments_router
from .robots.status import router as status_robot_router
from .step_types import router as step_types_router
from .robots.runs import router as robot_runs_router
from .robots.steps import router as robot_steps_router
from .robots.logs import router as robot_logs_router
from .robots.errors import router as robot_errors_router
from .auth import router as router_auth
