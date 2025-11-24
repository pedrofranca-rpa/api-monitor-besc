# app/db/base.py
# Centraliza o DeclarativeBase para todos os modelos

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base declarativa para todos os modelos SQLAlchemy.
    Centraliza metadados, configurações globais e facilita migrações.
    """

    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
