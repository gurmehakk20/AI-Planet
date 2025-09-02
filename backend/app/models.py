# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
