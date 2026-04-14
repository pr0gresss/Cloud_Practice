from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    __table_args__ = {"schema": "Dzmitry_Tsublianok_Feedbacks"}

    feedbackId = Column(Integer, primary_key=True)
    portfolioId = Column(Integer)
    content = Column(String)

    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, onupdate=func.now())