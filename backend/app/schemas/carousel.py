from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CarouselBase(BaseModel):
    """Base carousel item schema"""
    title: str
    description: Optional[str] = None
    image_url: str
    link_url: Optional[str] = None
    order: int = 0
    rotation_speed: int = 5000


class CarouselCreate(CarouselBase):
    """Carousel creation schema"""
    annotator_id: Optional[int] = None


class CarouselUpdate(BaseModel):
    """Carousel update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    annotator_id: Optional[int] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None
    rotation_speed: Optional[int] = None


class CarouselResponse(CarouselBase):
    """Carousel response schema"""
    id: int
    annotator_id: Optional[int] = None
    is_active: bool
    auto_rotate: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
