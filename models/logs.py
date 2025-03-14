from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Text, Column, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    inserted = Column(DateTime, default=datetime.utcnow, nullable=True)
    url = Column(Text, nullable=True)
    method = Column(Text, nullable=True)
    response = Column(Text, nullable=True)