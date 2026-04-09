from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.site_setting import SiteSetting
from app.schemas.site_setting import SiteBrandingResponse


router = APIRouter(prefix="/api/site-config", tags=["site-config"])


@router.get("/branding", response_model=SiteBrandingResponse)
async def get_branding(db: Session = Depends(get_db)):
    items = {
        item.key: item.value
        for item in db.query(SiteSetting).filter(
            SiteSetting.key.in_(["brand_logo_url", "admin_brand_logo_url"])
        ).all()
    }
    return SiteBrandingResponse(
        brand_logo_url=items.get("brand_logo_url"),
        admin_brand_logo_url=items.get("admin_brand_logo_url"),
    )
