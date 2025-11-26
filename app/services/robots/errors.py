# app/services/robot_errors.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.robots.errors import RobotError
from app.models.robots.steps import RobotStep

from app.schemas.robots.errors import RobotErrorCreate, RobotErrorUpdate, RobotErrorOut
from app.core.status import Status


class RobotErrorService:
    """
    Serviço assíncrono para operações CRUD de RobotErrors.
    """

    @staticmethod
    async def create(db: AsyncSession, data: RobotErrorCreate) -> RobotErrorOut:
        try:
            error = RobotError(**data.model_dump())
            db_step = await db.get(RobotStep, data.step_id)
            if not db_step:
                raise NoResultFound

            error.step_id = db_step.id
            db_step.status_id = Status.ERROR.value
            db.add(db_step)
            db.add(error)

            await db.commit()
            await db.refresh(error)
            await db.refresh(db_step)
            return RobotErrorOut.model_validate(error)

        except IntegrityError as err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar robot_error: violação de integridade." + str(err),
            )

        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar robot_error." + str(err),
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[RobotErrorOut]:
        try:
            query = select(RobotError).offset(skip)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)
            errors = result.scalars().all()

            return [RobotErrorOut.model_validate(e) for e in errors]

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao listar robot_errors.",
            )

    @staticmethod
    async def get(db: AsyncSession, error_id: int) -> RobotErrorOut:
        try:
            error = await db.get(RobotError, error_id)
            if not error:
                raise NoResultFound

            return RobotErrorOut.model_validate(error)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error not found",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao obter robot_error.",
            )

    @staticmethod
    async def update(
        db: AsyncSession, error_id: int, data: RobotErrorUpdate
    ) -> RobotErrorOut:
        try:
            error = await db.get(RobotError, error_id)
            if not error:
                raise NoResultFound

            update_data = data.model_dump(exclude_unset=True)

            if update_data:
                for key, value in update_data.items():
                    setattr(error, key, value)

                await db.commit()
                await db.refresh(error)

            return RobotErrorOut.model_validate(error)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar robot_error: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar robot_error.",
            )

    @staticmethod
    async def delete(db: AsyncSession, error_id: int) -> None:
        try:
            error = await db.get(RobotError, error_id)
            if not error:
                raise NoResultFound

            await db.delete(error)
            await db.commit()

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Error not found",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao deletar robot_error.",
            )
