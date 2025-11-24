# app/models/robot_runs.py

from sqlalchemy import Column, Integer, TIMESTAMP, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RobotRun(Base):
    __tablename__ = "robot_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    env_id = Column(SmallInteger, ForeignKey("environments.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status_robot.id"), nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    end_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    total_process = Column(Integer)
    host = Column(String(200))

    # Relationships
    bot = relationship("Bot", back_populates="runs")
    environment = relationship("Environment", back_populates="runs")
    status = relationship("StatusRobot", back_populates="runs")

    steps = relationship("RobotStep", back_populates="run", cascade="all, delete")
