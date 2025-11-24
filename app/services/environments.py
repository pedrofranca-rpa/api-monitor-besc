# app/services/environments.py

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.environments import Environment
from app.schemas.environments import (
    EnvironmentCreate,
    EnvironmentUpdate,
    EnvironmentOut,
)


class EnvironmentService:
    """
    Serviço assíncrono para operações CRUD relacionadas a Environments.
    Nota: Não há delete, pois a tabela é considerada crítica.
    """

    @staticmethod
    async def create(db: AsyncSession, data: EnvironmentCreate) -> EnvironmentOut:
        try:
            env = Environment(**data.model_dump())
            db.add(env)
            await db.commit()
            await db.refresh(env)
            return EnvironmentOut.model_validate(env)

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar environment: duplicado ou violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar environment.",
            )

    @staticmethod
    async def list(
        db: AsyncSession, skip: int = 0, limit: Optional[int] = None
    ) -> List[EnvironmentOut]:
        try:
            query = select(Environment).offset(skip)
            if limit is not None:
                query = query.limit(limit)

            result = await db.execute(query)
            envs = result.scalars().all()

            return [EnvironmentOut.model_validate(e) for e in envs]

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao listar environments.",
            )

    @staticmethod
    async def get(db: AsyncSession, env_id: int) -> EnvironmentOut:
        try:
            env = await db.get(Environment, env_id)
            if not env:
                raise NoResultFound
            return EnvironmentOut.model_validate(env)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Environment not found",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao obter environment.",
            )

    @staticmethod
    async def update(
        db: AsyncSession, env_id: int, data: EnvironmentUpdate
    ) -> EnvironmentOut:
        try:
            env = await db.get(Environment, env_id)
            if not env:
                raise NoResultFound

            update_data = data.model_dump(exclude_unset=True)

            if update_data:
                for key, value in update_data.items():
                    setattr(env, key, value)

                await db.commit()
                await db.refresh(env)

            return EnvironmentOut.model_validate(env)

        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Environment not found",
            )

        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar environment: violação de integridade.",
            )

        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar environment.",
            )
