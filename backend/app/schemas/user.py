from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
