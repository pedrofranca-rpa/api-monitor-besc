# app/services/status_robot.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.robots.status import StatusRobot
from app.schemas.robots.status import (
    StatusRobotCreate,
    StatusRobotUpdate,
    StatusRobotOut,
)


class StatusRobotService:
    """
    Serviço assíncrono para operações CRUD de StatusRobot.
    (Sem delete — tabela crítica.)
    """

    @staticmethod
    async def create(db: AsyncSession, data: StatusRobotCreate) -> StatusRobotOut:
        try:
            status_robot = StatusRobot(**data.model_dump())
            db.add(status_robot)
            await db.commit()
            await db.refresh(status_robot)
            return StatusRobotOut.model_validate(status_robot)

        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar status_robot: violação de integridade.",
            )

        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao criar status_robot.",
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[StatusRobotOut]:
        try:
            query = select(StatusRobot).offset(skip)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)
            statuses = result.scalars().all()

            return [StatusRobotOut.model_validate(s) for s in statuses]

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao listar status_robots.",
            )

    @staticmethod
    async def get(db: AsyncSession, status_id: str) -> StatusRobotOut:
        try:
            status_robot = await db.get(StatusRobot, status_id)
            if not status_robot:
                raise NoResultFound

            return StatusRobotOut.model_validate(status_robot)

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Status not found",
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao obter status_robot.",
            )

    @staticmethod
    async def update(
        db: AsyncSession, status_id: str, data: StatusRobotUpdate
    ) -> StatusRobotOut:
        try:
            status_robot = await db.get(StatusRobot, status_id)
            if not status_robot:
                raise NoResultFound

            updates = data.model_dump(exclude_unset=True)

            if updates:
                for key, value in updates.items():
                    setattr(status_robot, key, value)

                await db.commit()
                await db.refresh(status_robot)

            return StatusRobotOut.model_validate(status_robot)

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Status not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro ao atualizar status_robot: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao atualizar status_robot.",
            )
