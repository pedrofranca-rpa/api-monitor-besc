# app/routers/step_types.py
# Router FastAPI para CRUD de 'step_types'.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.step_types import StepTypeService
from app.schemas.step_types import StepTypeCreate, StepTypeUpdate, StepTypeOut

router = APIRouter(prefix="/step-types", tags=["step_types"])


@router.post("/", response_model=StepTypeOut)
async def create_step_type(step_type: StepTypeCreate, db: Session = Depends(get_db)):
    try:
        return await StepTypeService.create(db, step_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StepTypeOut])
async def list_step_types(db: Session = Depends(get_db)):
    return await StepTypeService.list(db)


@router.get("/{step_type_id}", response_model=StepTypeOut)
async def get_step_type(step_type_id: int, db: Session = Depends(get_db)):
    try:
        return await StepTypeService.get(db, step_type_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{step_type_id}", response_model=StepTypeOut)
async def update_step_type(
    step_type_id: int, step_type: StepTypeUpdate, db: Session = Depends(get_db)
):
    try:
        return await StepTypeService.update(db, step_type_id, step_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Sem delete.
