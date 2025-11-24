# app/services/robot_steps.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from sqlalchemy.orm import selectinload

from app.core.status import Status
from app.models.robots.steps import RobotStep
from app.schemas.robots.steps import RobotStepCreate, RobotStepUpdate, RobotStepOut


class RobotStepService:
    """
    Serviço assíncrono para CRUD de RobotSteps.
    """

    @staticmethod
    async def create(db: AsyncSession, step: RobotStepCreate) -> RobotStepOut:
        try:
            db_step = RobotStep(**step.model_dump())
            db_step.status_id = Status.PENDING.value
            db.add(db_step)
            await db.commit()
            await db.refresh(db_step)
            return RobotStepOut.model_validate(db_step)

        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar robot_step: violação de integridade." + str(err),
            )

        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao criar robot_step." + str(err),
            )

    @staticmethod
    async def finish(db: AsyncSession, step_id: int) -> RobotStepOut:
        try:
            step = await db.get(RobotStep, step_id)
            if not step:
                raise NoResultFound

            step.status_id = Status.SUCCESS.value

            await db.commit()
            await db.refresh(step)

            return RobotStepOut.model_validate(step)

        except NoResultFound:
            raise HTTPException(
                status_code=step.HTTP_404_NOT_FOUND,
                detail="Step not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar robot_step: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar robot_step.",
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[RobotStepOut]:
        try:
            query = select(RobotStep).offset(skip)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)
            steps = result.scalars().all()

            return [RobotStepOut.model_validate(s) for s in steps]

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao listar robot_steps.",
            )

    @staticmethod
    async def get(db: AsyncSession, step_id: int) -> RobotStepOut:
        try:
            # Carrega o step + logs em uma query otimizada
            result = await db.execute(
                select(RobotStep)
                .options(selectinload(RobotStep.logs))
                .where(RobotStep.id == step_id)
            )

            step = result.scalars().first()

            if not step:
                raise NoResultFound

            return RobotStepOut.model_validate(step)

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Step not found",
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao obter robot_step. {str(e)}",
            )

    @staticmethod
    async def update(
        db: AsyncSession, step_id: int, step_update: RobotStepUpdate
    ) -> RobotStepOut:

        try:
            db_step = await db.get(RobotStep, step_id)
            if not db_step:
                raise NoResultFound

            update_data = step_update.model_dump(exclude_unset=True)

            if update_data:
                for key, value in update_data.items():
                    setattr(db_step, key, value)

                await db.commit()
                await db.refresh(db_step)

            return RobotStepOut.model_validate(db_step)

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Step not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro ao atualizar robot_step: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao atualizar robot_step.",
            )

    @staticmethod
    async def delete(db: AsyncSession, step_id: int):
        try:
            db_step = await db.get(RobotStep, step_id)
            if not db_step:
                raise NoResultFound

            await db.delete(db_step)
            await db.commit()

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Step not found",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao deletar robot_step.",
            )
