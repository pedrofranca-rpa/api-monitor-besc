# app/models/step_types.py
# Modelo SQLAlchemy para a tabela 'step_types'.

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db import Base


class StepType(Base):
    __tablename__ = "step_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Relationship: Um step_type tem muitos steps.
    steps = relationship("RobotStep", back_populates="step_type")
