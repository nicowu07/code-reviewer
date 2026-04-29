from sqlalchemy import Column, Integer, JSON, DateTime, String
from app.database.connection import Base
from datetime import datetime
from uuid import uuid4

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    lines_of_code = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    severity_high = Column(Integer)
    severity_medium = Column(Integer)
    severity_low = Column(Integer)
    issues = Column(JSON)
    ai_analysis = Column(JSON, nullable=True)

