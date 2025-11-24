# app/models/bots.py

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    status = Column(Boolean, nullable=False)
    # Relationship
    runs = relationship("RobotRun", back_populates="bot")
