# app/models/robot_errors.py
# Modelo SQLAlchemy para a tabela 'robot_errors'.

from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db import Base


class RobotError(Base):
    __tablename__ = "robot_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(Integer, ForeignKey("robot_logs.id"), nullable=False)

    function = Column(String(200))
    class_excpt = Column(String(200))
    traceback = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False)

    # Relationship.
    log = relationship("RobotLog", back_populates="errors")
