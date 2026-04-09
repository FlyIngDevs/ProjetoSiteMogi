from pydantic import BaseModel


class SiteBrandingResponse(BaseModel):
    brand_logo_url: str | None = None
    admin_brand_logo_url: str | None = None


class SiteBrandingUpdate(BaseModel):
    brand_logo_url: str | None = None
    admin_brand_logo_url: str | None = None
