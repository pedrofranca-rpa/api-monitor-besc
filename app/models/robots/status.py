from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class StatusRobot(Base):
    __tablename__ = "status_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)

    runs = relationship("RobotRun", back_populates="status")
    steps = relationship("RobotStep", back_populates="status")
    logs = relationship("RobotLog", back_populates="status")
