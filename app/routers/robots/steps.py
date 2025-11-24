# app/routers/robot_steps.py
# Router FastAPI para CRUD de 'robot_steps' e endpoint especial.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.robots.steps import RobotStepService
from app.schemas.robots.steps import RobotStepCreate, RobotStepUpdate, RobotStepOut

router = APIRouter(prefix="/steps", tags=["robot_steps"])


@router.post("/create", response_model=RobotStepOut)
async def create_step(step: RobotStepCreate, db: Session = Depends(get_db)):
    try:
        return await RobotStepService.create(db, step)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{step_id}/finish", response_model=RobotStepOut)
async def finish_step(step_id: int, db: Session = Depends(get_db)):
    try:
        return await RobotStepService.finish(db, step_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{step_id}", response_model=RobotStepOut)
async def get_step(step_id: int, db: Session = Depends(get_db)):
    try:
        return await RobotStepService.get(db, step_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{step_id}", response_model=RobotStepOut)
async def update_step(
    step_id: int, step: RobotStepUpdate, db: Session = Depends(get_db)
):
    try:
        return await RobotStepService.update(db, step_id, step)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{step_id}")
async def delete_step(step_id: int, db: Session = Depends(get_db)):
    try:
        RobotStepService.delete(db, step_id)
        return await {"detail": "Step deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Endpoint especial para /runs/{run_id}/step (cria ou atualiza).
@router.post("/{run_id}/step", response_model=RobotStepOut)
async def handle_step(
    run_id: int, step: RobotStepCreate, db: Session = Depends(get_db)
):
    # Assumindo que cria novo; se precisar atualizar, verifique existência.
    if step.run_id != run_id:
        raise HTTPException(status_code=400, detail="Run ID mismatch")
    return await create_step(step, db)
