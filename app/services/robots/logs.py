# app/services/robot_logs.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from app.core.status import Status
from app.models.robots.logs import RobotLog
from app.models.robots.steps import RobotStep
from app.schemas.robots.logs import RobotLogCreate, RobotLogUpdate, RobotLogOut
from app.schemas.robots.steps import RobotStepOut


class RobotLogService:
    """
    Serviço assíncrono para CRUD de RobotLogs.
    """

    @staticmethod
    async def create(db: AsyncSession, data: RobotLogCreate) -> RobotLogOut:
        try:
            log = RobotLog(**data.model_dump())
            log.status_id = Status.PENDING.value
            db.add(log)
            await db.commit()
            await db.refresh(log)
            return RobotLogOut.model_validate(log)

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar robot_log: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar robot_log.",
            )

    @staticmethod
    async def finish(db: AsyncSession, log_id: int) -> RobotLogOut:
        try:
            log = await db.get(RobotLog, log_id)
            if not log:
                raise NoResultFound

            log.status_id = Status.SUCCESS.value

            await db.commit()
            await db.refresh(log)

            return RobotLogOut.model_validate(log)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Log not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar robot_log: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar robot_log.",
            )
