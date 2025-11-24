# app/routers/robot_runs.py
# Router FastAPI para CRUD de 'robot_runs' e endpoints especiais.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.robots.runs import RobotRunService
from app.schemas.robots.runs import RobotRunCreate, RobotRunOut, RobotRunUpdate

router = APIRouter(prefix="/runs", tags=["robots_runs"])


@router.post("/", response_model=RobotRunOut)
async def create_run(run: RobotRunCreate, db: Session = Depends(get_db)):
    try:
        return await RobotRunService.create(db, run)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RobotRunOut])
async def list_runs(db: Session = Depends(get_db)):
    return await RobotRunService.list(db)


@router.get("/{run_id}", response_model=RobotRunOut)
async def get_run(run_id: int, db: Session = Depends(get_db)):
    try:
        return await RobotRunService.get(db, run_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/start", response_model=RobotRunOut)
async def start_run(run: RobotRunCreate, db: Session = Depends(get_db)):
    # Cria um novo run (mesmo que create, mas endpoint específico).
    return await create_run(run, db)


@router.post("/{run_id}/finish")
async def finish_run(run_id: int, data: RobotRunUpdate, db: Session = Depends(get_db)):
    try:
        return await RobotRunService.finish(db, run_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
