from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base


class Carousel(Base):
    """Carousel item model - for home page carousel"""
    __tablename__ = "carousel_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String)
    link_url = Column(String, nullable=True)
    
    # Reference to annotator (company/vendor)
    annotator_id = Column(Integer, ForeignKey("annotators.id"), nullable=True)
    
    # Display settings
    order = Column(Integer, default=0)  # Display order
    is_active = Column(Boolean, default=True)
    auto_rotate = Column(Boolean, default=True)
    rotation_speed = Column(Integer, default=5000)  # milliseconds
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
