# app/models/robot_logs.py

from sqlalchemy import Column, Integer, String, Numeric, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RobotLog(Base):
    __tablename__ = "robot_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys necessárias
    step_id = Column(Integer, ForeignKey("robot_steps.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status_robot.id"), nullable=True)

    function = Column(String(200))
    filename = Column(String(300))
    time_ms = Column(Numeric)
    docs = Column(Text)
    evidence = Column(Text)

    # Relationships
    steps = relationship("RobotStep", back_populates="logs")
    status = relationship("StatusRobot", back_populates="logs")

