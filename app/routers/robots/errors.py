# app/routers/robot_errors.py
# Router FastAPI para CRUD de 'robot_errors' e endpoint especial.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.robots.errors import RobotErrorService
from app.schemas.robots.errors import RobotErrorCreate, RobotErrorUpdate, RobotErrorOut

router = APIRouter(prefix="/errors", tags=["robot_errors"])


@router.post("/", response_model=RobotErrorOut)
async def create_error(error: RobotErrorCreate, db: Session = Depends(get_db)):
    try:
        return await RobotErrorService.create(db, error)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RobotErrorOut])
async def list_errors(db: Session = Depends(get_db)):
    return await RobotErrorService.list(db)


@router.get("/{error_id}", response_model=RobotErrorOut)
async def get_error(error_id: int, db: Session = Depends(get_db)):
    try:
        return await RobotErrorService.get(db, error_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{error_id}", response_model=RobotErrorOut)
async def update_error(
    error_id: int, error: RobotErrorUpdate, db: Session = Depends(get_db)
):
    try:
        return await RobotErrorService.update(db, error_id, error)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{error_id}")
async def delete_error(error_id: int, db: Session = Depends(get_db)):
    try:
        RobotErrorService.delete(db, error_id)
        return await {"detail": "Error deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Endpoint especial para /runs/{run_id}/error.
@router.post("/{run_id}/error", response_model=RobotErrorOut)
async def handle_error(
    run_id: int, error: RobotErrorCreate, db: Session = Depends(get_db)
):
    # Note: Não valida run_id diretamente, pois error é ligado a log_id.
    return await create_error(error, db)
