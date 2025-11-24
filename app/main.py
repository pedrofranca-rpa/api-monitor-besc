# app/main.py
# Arquivo principal da aplicação FastAPI.

from fastapi import FastAPI


from app.core.security import jwt_middleware
from app.database import init_db

from app.routers import (
    bots_router,
    environments_router,
    status_robot_router,
    step_types_router,
    robot_runs_router,
    robot_steps_router,
    robot_logs_router,
    robot_errors_router,
    router_auth,
)

app = FastAPI(title="Robot Monitoring API")

app.middleware("http")(jwt_middleware)
# Inclui todos os routers.
app.include_router(bots_router)
app.include_router(environments_router)
app.include_router(status_robot_router)
app.include_router(step_types_router)
app.include_router(robot_runs_router)
app.include_router(robot_steps_router)
app.include_router(robot_logs_router)
app.include_router(robot_errors_router)
app.include_router(router_auth)


# ====================================
# EVENTOS DE CICLO DE VIDA DO FASTAPI
# ====================================
@app.on_event("startup")
async def on_startup():
    """Executa ao iniciar a aplicação."""
    await init_db()  # Cria as tabelas se ainda não existirem
    print("✅ Banco de dados inicializado com sucesso!")


@app.on_event("shutdown")
async def on_shutdown():
    """Executa ao encerrar a aplicação."""
    print("🛑 Encerrando aplicação...")
