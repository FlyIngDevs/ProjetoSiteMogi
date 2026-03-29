from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database.database import Base


class Annotator(Base):
    """Annotator/Company model - represents vendors in the platform"""
    __tablename__ = "annotators"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)  # For micro site URL
    description = Column(Text)
    logo_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    photo_1_url = Column(String, nullable=True)
    photo_2_url = Column(String, nullable=True)
    photo_3_url = Column(String, nullable=True)
    photo_4_url = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    website = Column(String, nullable=True)
    
    # Location
    city = Column(String)
    state = Column(String)
    address = Column(String, nullable=True)
    
    # Social media
    facebook_url = Column(String, nullable=True)
    instagram_url = Column(String, nullable=True)
    whatsapp_number = Column(String, nullable=True)
    twitter_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
