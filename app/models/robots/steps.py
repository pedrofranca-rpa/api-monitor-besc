from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class RobotStep(Base):
    __tablename__ = "robot_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys obrigatórias
    run_id = Column(Integer, ForeignKey("robot_runs.id"), nullable=False)
    step_type_id = Column(Integer, ForeignKey("step_types.id"), nullable=True)
    status_id = Column(Integer, ForeignKey("status_robot.id"), nullable=False)

    ended_at = Column(TIMESTAMP)

    # Relationships
    logs = relationship("RobotLog", back_populates="steps")
    run = relationship("RobotRun", back_populates="steps")
    step_type = relationship("StepType", back_populates="steps")
    status = relationship("StatusRobot", back_populates="steps")
