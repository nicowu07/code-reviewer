from sqlalchemy import Column, Integer, JSON, DateTime
from app.database.connection import Base
from datetime import datetime

class Scan(Base):
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True)
    lines_of_code = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    severity_high = Column(Integer)
    severity_medium = Column(Integer)
    severity_low = Column(Integer)
    issues = Column(JSON)

