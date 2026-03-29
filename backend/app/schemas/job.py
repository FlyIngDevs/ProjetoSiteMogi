from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class JobWriteBase(BaseModel):
    """Base job schema for create/update validation"""
    title: str
    description: str
    category: str
    employment_type: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: str
    state: str
    company_name: str
    company_email: EmailStr
    company_phone: str
    requirements: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None


class JobCreate(JobWriteBase):
    """Job creation schema"""
    company_id: Optional[int] = None


class JobUpdate(BaseModel):
    """Job update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    employment_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    company_email: Optional[EmailStr] = None
    company_phone: Optional[str] = None
    requirements: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class JobResponse(BaseModel):
    """Job response schema"""
    id: int
    title: str
    description: str
    category: str
    employment_type: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    city: str
    state: str
    company_name: str
    company_email: str
    company_phone: str
    requirements: str
    contact_email: str
    contact_phone: Optional[str] = None
    company_id: Optional[int] = None
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class JobMiniResponse(BaseModel):
    """Minimal job response for lists"""
    id: int
    title: str
    description: str
    company_name: str
    city: str
    category: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    
    class Config:
        from_attributes = True
