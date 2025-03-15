from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column, DateTime, Numeric, DECIMAL
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Candles(Base):
    __tablename__ = "candles"
    id = Column(Integer, primary_key=True)
    inserted = Column(DateTime, default=datetime.utcnow, nullable=True)
    high = Column(DECIMAL(precision=20, scale=5), nullable=True)
    close = Column(DECIMAL(precision=20, scale=5), nullable=True)
    low = Column(DECIMAL(precision=20, scale=5), nullable=True)
    open = Column(DECIMAL(precision=20, scale=5), nullable=True)
    volume = Column(DECIMAL(precision=20, scale=5), nullable=True)
    timestamp = Column(Integer, nullable=True)
    pair = Column(String(30), nullable=True)