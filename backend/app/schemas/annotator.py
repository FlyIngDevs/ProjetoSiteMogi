from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class AnnotatorBase(BaseModel):
    """Base annotator schema"""
    company_name: str
    slug: str
    description: str
    email: EmailStr
    phone: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    photo_1_url: Optional[str] = None
    photo_2_url: Optional[str] = None
    photo_3_url: Optional[str] = None
    photo_4_url: Optional[str] = None
    city: str
    state: str
    address: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None


class AnnotatorCreate(AnnotatorBase):
    """Annotator creation schema"""
    is_active: bool = True
    is_verified: bool = False


class AnnotatorUpdate(BaseModel):
    """Annotator update schema"""
    company_name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    photo_1_url: Optional[str] = None
    photo_2_url: Optional[str] = None
    photo_3_url: Optional[str] = None
    photo_4_url: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class AnnotatorResponse(AnnotatorBase):
    """Annotator response schema"""
    id: int
    is_active: bool
    is_verified: bool
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    photo_1_url: Optional[str] = None
    photo_2_url: Optional[str] = None
    photo_3_url: Optional[str] = None
    photo_4_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AnnotatorMiniResponse(BaseModel):
    """Minimal annotator response for lists"""
    id: int
    company_name: str
    slug: str
    description: str
    city: str
    state: str
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    facebook_url: Optional[str] = None
    instagram_url: Optional[str] = None
    whatsapp_number: Optional[str] = None
    
    class Config:
        from_attributes = True
