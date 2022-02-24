from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base


class TvScreenerSignals(Base):
    __tablename__ = "tv_screener_relative_volume15m"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    how_many = Column(Integer, nullable=False, default=0)
    price = Column(Float)
    percent = Column(Integer, nullable=False, default=0)
