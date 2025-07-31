
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, index=True)
    image_path = Column(String)
    report = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
