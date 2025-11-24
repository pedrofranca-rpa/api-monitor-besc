# app/routers/bots.py
# Router FastAPI para CRUD de 'bots'.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.bots import BotService
from app.schemas.bots import BotCreate, BotUpdate, BotOut

router = APIRouter(prefix="/bots", tags=["bots"])


@router.post("/", response_model=BotOut)
async def create_bot(bot: BotCreate, db: Session = Depends(get_db)):
    try:
        return await BotService.create(db, bot)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[BotOut])
async def list_bots(db: Session = Depends(get_db)):
    return await BotService.list(db)


@router.get("/{bot_id}", response_model=BotOut)
async def get_bot(bot_id: int, db: Session = Depends(get_db)):
    try:
        return await BotService.get(db, bot_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{bot_id}", response_model=BotOut)
async def update_bot(bot_id: int, bot: BotUpdate, db: Session = Depends(get_db)):
    try:
        update = await BotService.update(db, bot_id, bot)
        return update
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{bot_id}")
async def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    try:
        await BotService.delete(db, bot_id)
        return {"detail": "Bot deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
