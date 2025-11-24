# app/services/bots.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.bots import Bot
from app.schemas.bots import BotCreate, BotUpdate, BotOut


class BotService:
    """
    Serviço assíncrono para operações CRUD de Bots.
    Compatível com SQLAlchemy Async 2.0.
    """

    @staticmethod
    async def create(db: AsyncSession, data: BotCreate) -> BotOut:
        try:
            bot = Bot(**data.model_dump())
            bot.status = True
            db.add(bot)
            await db.commit()
            await db.refresh(bot)
            return BotOut.model_validate(bot)

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar bot: nome duplicado ou violação de integridade.",
            )

        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar bot -> " + err,
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[BotOut]:
        try:
            query = select(Bot).offset(skip)
            if limit is not None:
                query = query.limit(limit)

            result = await db.execute(query)
            bots = result.scalars().all()

            return [BotOut.model_validate(b) for b in bots]

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao listar bots.",
            )

    @staticmethod
    async def get(db: AsyncSession, bot_id: int) -> BotOut:
        try:
            bot = await db.get(Bot, bot_id)
            if not bot:
                raise NoResultFound
            return BotOut.model_validate(bot)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot not found",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao obter bot.",
            )

    @staticmethod
    async def update(db: AsyncSession, bot_id: int, data: BotUpdate) -> BotOut:
        try:
            bot = await db.get(Bot, bot_id)
            if not bot:
                raise NoResultFound

            updates = data.model_dump(exclude_unset=True)
            if updates:
                for key, value in updates.items():
                    setattr(bot, key, value)

                await db.commit()
                await db.refresh(bot)

            return BotOut.model_validate(bot)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar bot: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar bot.",
            )

    @staticmethod
    async def delete(db: AsyncSession, bot_id: int) -> None:
        try:
            bot = await db.get(Bot, bot_id)
            if not bot:
                raise NoResultFound

            await db.delete(bot)
            await db.commit()

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bot not found",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao deletar bot.",
            )
