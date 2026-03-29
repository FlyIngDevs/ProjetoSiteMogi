from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base


class Job(Base):
    """Job posting model - classified jobs"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)  # e.g., sales, it, marketing
    employment_type = Column(String)  # full-time, part-time, freelance
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    
    # Location
    city = Column(String)
    state = Column(String)
    
    # Company info
    company_id = Column(Integer, ForeignKey("annotators.id"), nullable=True)
    company_name = Column(String)
    company_email = Column(String)
    company_phone = Column(String)
    
    # Contact & requirements
    requirements = Column(Text)
    contact_email = Column(String)
    contact_phone = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # Featured job
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
