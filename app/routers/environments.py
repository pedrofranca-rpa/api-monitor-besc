# app/routers/environments.py
# Router FastAPI para CRUD de 'environments'.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.environments import EnvironmentService
from app.schemas.environments import (
    EnvironmentCreate,
    EnvironmentUpdate,
    EnvironmentOut,
)

router = APIRouter(prefix="/environments", tags=["environments"])


@router.post("/", response_model=EnvironmentOut)
async def create_environment(env: EnvironmentCreate, db: Session = Depends(get_db)):
    try:
        return await EnvironmentService.create(db, env)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[EnvironmentOut])
async def list_environments(db: Session = Depends(get_db)):
    return await EnvironmentService.list(db)


@router.get("/{env_id}", response_model=EnvironmentOut)
async def get_environment(env_id: int, db: Session = Depends(get_db)):
    try:
        return await EnvironmentService.get(db, env_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{env_id}", response_model=EnvironmentOut)
async def update_environment(
    env_id: int, env: EnvironmentUpdate, db: Session = Depends(get_db)
):
    try:
        return await EnvironmentService.update(db, env_id, env)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Sem delete.
