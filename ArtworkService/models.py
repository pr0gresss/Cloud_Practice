from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base

class Artwork(Base):
    __tablename__ = "artworks"
    __table_args__ = {"schema": "Dzmitry_Tsublianok_Artworks"}

    artworkId = Column(Integer, primary_key=True)
    portfolioId = Column(Integer)
    imageUrl = Column(String)
    title = Column(String)
    description = Column(String)
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, onupdate=func.now())