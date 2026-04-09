from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_admin
from app.database.database import get_db
from app.models.site_setting import SiteSetting
from app.models.user import User
from app.schemas.site_setting import SiteBrandingResponse, SiteBrandingUpdate


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


@router.put("/branding", response_model=SiteBrandingResponse)
async def update_branding(
    branding: SiteBrandingUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """Update site branding (admin only)."""
    # Update brand_logo_url
    if branding.brand_logo_url is not None:
        logo_setting = db.query(SiteSetting).filter(
            SiteSetting.key == "brand_logo_url"
        ).first()
        if logo_setting:
            logo_setting.value = branding.brand_logo_url
        else:
            logo_setting = SiteSetting(key="brand_logo_url", value=branding.brand_logo_url)
            db.add(logo_setting)

    # Update admin_brand_logo_url
    if branding.admin_brand_logo_url is not None:
        admin_logo_setting = db.query(SiteSetting).filter(
            SiteSetting.key == "admin_brand_logo_url"
        ).first()
        if admin_logo_setting:
            admin_logo_setting.value = branding.admin_brand_logo_url
        else:
            admin_logo_setting = SiteSetting(key="admin_brand_logo_url", value=branding.admin_brand_logo_url)
            db.add(admin_logo_setting)

    db.commit()

    # Return updated values
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
