from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.sql import func

from app.database.database import Base


class SiteSetting(Base):
    """Simple key/value store for site-wide branding and configuration."""

    __tablename__ = "site_settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
