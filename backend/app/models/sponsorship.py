from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from app.database.database import Base


class Sponsorship(Base):
    """Sponsorship model - fixed sponsorships on home page"""
    __tablename__ = "sponsorships"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    logo_url = Column(String)
    banner_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    website_url = Column(String, nullable=True)
    
    # Sponsorship details
    position = Column(String, default="banner")  # banner, sidebar, footer
    order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Dates
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
