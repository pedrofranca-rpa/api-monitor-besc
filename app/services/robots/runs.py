# app/services/robot_runs.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
from app.core.status import Status
from app.models.robots.runs import RobotRun
from app.schemas.robots.runs import RobotRunCreate, RobotRunUpdate, RobotRunOut


class RobotRunService:
    """
    Serviço assíncrono para gerenciamento de RobotRuns (execuções do robô).
    """

    @staticmethod
    async def create(db: AsyncSession, data: RobotRunCreate) -> RobotRunOut:
        try:
            run = RobotRun(**data.model_dump())
            run.status_id = Status.PENDING.value
            db.add(run)
            await db.commit()
            await db.refresh(run)
            return RobotRunOut.model_validate(run)

        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar robot_run: violação de integridade. " + str(err),
            )

        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao criar robot_run." + str(err),
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[RobotRunOut]:
        try:
            query = select(RobotRun).offset(skip)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)
            runs = result.scalars().all()

            return [RobotRunOut.model_validate(r) for r in runs]

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao listar robot_runs.",
            )

    @staticmethod
    async def get(db: AsyncSession, run_id: int) -> RobotRunOut:
        try:
            run = await db.get(RobotRun, run_id)
            if not run:
                raise NoResultFound

            return RobotRunOut.model_validate(run)

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Run not found",
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao obter robot_run.",
            )

    @staticmethod
    async def update(
        db: AsyncSession, run_id: int, data: RobotRunUpdate
    ) -> RobotRunUpdate:

        try:
            run = await db.get(RobotRun, run_id)
            if not run:
                raise NoResultFound

            if run.status_id == Status.SUCCESS.value:
                raise HTTPException(
                    status_code=409,
                    detail="Processo já foi finalizado anteriormente!",
                )

            update_data = data.model_dump(exclude_unset=True)

            if update_data:
                for key, value in update_data.items():
                    setattr(run, key, value)

                await db.commit()
                await db.refresh(run)

            return RobotRunOut.model_validate(run)

        except NoResultFound as error:
            raise HTTPException(
                status_code=404,
                detail="Run not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Erro ao atualizar robot_run: violação de integridade.",
            )

        except Exception as error:
            await db.rollback()
            raise error

    @staticmethod
    async def delete(db: AsyncSession, run_id: int) -> None:
        try:
            run = await db.get(RobotRun, run_id)
            if not run:
                raise NoResultFound

            await db.delete(run)
            await db.commit()

        except NoResultFound:
            raise HTTPException(
                status_code=404,
                detail="Run not found",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao deletar robot_run.",
            )

    # --------------------------------------------------------
    # MÉTODO ESPECIAL PARA FINALIZAR UMA EXECUÇÃO DO ROBÔ
    # --------------------------------------------------------
    @staticmethod
    async def finish(
        db: AsyncSession, run_id: int, data: RobotRunUpdate
    ) -> RobotRunOut:
        """
        Finaliza uma execução do robô:
        - define end_at
        - atualiza status
        - atualiza total_process
        """

        from datetime import datetime

        update_payload = RobotRunUpdate(
            end_at=datetime.now(),
            status_id=Status.SUCCESS.value,
            total_process=data.total_process,
        )

        return await RobotRunService.update(db, run_id, update_payload)
