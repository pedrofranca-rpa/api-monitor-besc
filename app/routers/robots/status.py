# app/routers/status_robot.py
# Router FastAPI para CRUD de 'status_robot'.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.robots.status import StatusRobotService
from app.schemas.robots.status import (
    StatusRobotCreate,
    StatusRobotUpdate,
    StatusRobotOut,
)

router = APIRouter(prefix="/status-robot", tags=["status_robot"])


@router.post("/", response_model=StatusRobotOut)
async def create_status(status: StatusRobotCreate, db: Session = Depends(get_db)):
    try:
        return await StatusRobotService.create(db, status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StatusRobotOut])
async def list_status(db: Session = Depends(get_db)):
    return await StatusRobotService.list(db)


@router.get("/{status_id}", response_model=StatusRobotOut)
async def get_status(status_id: str, db: Session = Depends(get_db)):
    try:
        return await StatusRobotService.get(db, status_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{status_id}", response_model=StatusRobotOut)
async def update_status(
    status_id: str, status: StatusRobotUpdate, db: Session = Depends(get_db)
):
    try:
        return await StatusRobotService.update(db, status_id, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Sem delete.
