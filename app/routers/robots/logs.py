# app/routers/robot_logs.py
# Router FastAPI para CRUD de 'robot_logs' e endpoint especial.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.robots.logs import RobotLogService
from app.schemas.robots.logs import RobotLogCreate, RobotLogUpdate, RobotLogOut

router = APIRouter(prefix="/logs", tags=["robot_logs"])


@router.post("/create", response_model=RobotLogOut)
async def create_log(log: RobotLogCreate, db: Session = Depends(get_db)):
    try:
        return await RobotLogService.create(db, log)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{log_id}/finish", response_model=RobotLogOut)
async def create_log(log_id: int, db: Session = Depends(get_db)):
    try:
        return await RobotLogService.finish(db, log_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
