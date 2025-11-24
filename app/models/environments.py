# app/models/environments.py
# Modelo SQLAlchemy para a tabela 'environments'.

from sqlalchemy import Column, SmallInteger, String, Text
from sqlalchemy.orm import relationship

from app.db import Base


class Environment(Base):
    __tablename__ = "environments"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)

    # Relationship: Um environment tem muitas runs.
    runs = relationship("RobotRun", back_populates="environment")
