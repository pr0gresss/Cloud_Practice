from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base


class Portfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = {"schema": "Dzmitry_Tsublianok_Portfolios"}

    portfolioId = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())