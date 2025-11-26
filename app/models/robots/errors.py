# app/models/robot_errors.py
# Modelo SQLAlchemy para a tabela 'robot_errors'.

from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship

from app.db.base import Base
# app/models/robot_errors.py
class RobotError(Base):
    __tablename__ = "robot_errors"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    step_id = Column(Integer, ForeignKey("robot_steps.id"), nullable=False, unique=True)
    function = Column(String(200))
    class_excpt = Column(String(200))
    traceback = Column(Text)

    # Correto:
    steps = relationship("RobotStep", back_populates="error")
