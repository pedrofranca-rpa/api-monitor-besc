# app/services/step_types.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.step_types import StepType
from app.schemas.step_types import StepTypeCreate, StepTypeUpdate, StepTypeOut


class StepTypeService:
    """
    Serviço assíncrono para CRUD de StepTypes (tipos de passos).
    Não possui delete, pois é tabela crítica.
    """

    @staticmethod
    async def create(db: AsyncSession, data: StepTypeCreate) -> StepTypeOut:
        try:
            step_type = StepType(**data.model_dump())
            db.add(step_type)
            await db.commit()
            await db.refresh(step_type)
            return StepTypeOut.model_validate(step_type)

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar step_type: duplicado ou violação de restrição.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar step_type.",
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[StepTypeOut]:
        try:
            query = select(StepType).offset(skip)
            if limit:
                query = query.limit(limit)

            result = await db.execute(query)
            types = result.scalars().all()

            return [StepTypeOut.model_validate(st) for st in types]

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao listar step_types.",
            )

    @staticmethod
    async def get(db: AsyncSession, step_type_id: int) -> StepTypeOut:
        try:
            step_type = await db.get(StepType, step_type_id)
            if not step_type:
                raise NoResultFound

            return StepTypeOut.model_validate(step_type)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="StepType not found",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao obter step_type.",
            )

    @staticmethod
    async def update(
        db: AsyncSession, step_type_id: int, data: StepTypeUpdate
    ) -> StepTypeOut:
        try:
            step_type = await db.get(StepType, step_type_id)
            if not step_type:
                raise NoResultFound

            update_data = data.model_dump(exclude_unset=True)

            if update_data:
                for key, value in update_data.items():
                    setattr(step_type, key, value)

                await db.commit()
                await db.refresh(step_type)

            return StepTypeOut.model_validate(step_type)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="StepType not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar step_type: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar step_type.",
            )
