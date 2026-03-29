from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SponsorshipBase(BaseModel):
    """Base sponsorship schema"""
    company_name: str
    logo_url: str
    banner_url: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    position: str = "banner"
    order: int = 0


class SponsorshipCreate(SponsorshipBase):
    """Sponsorship creation schema"""
    start_date: datetime
    end_date: Optional[datetime] = None


class SponsorshipUpdate(BaseModel):
    """Sponsorship update schema"""
    company_name: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    position: Optional[str] = None
    order: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class SponsorshipResponse(SponsorshipBase):
    """Sponsorship response schema"""
    id: int
    is_active: bool
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
