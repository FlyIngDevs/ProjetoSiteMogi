from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging
from urllib.parse import urlparse

from app.core.security import get_current_admin
from app.database.database import get_db
from app.models.site_setting import SiteSetting
from app.models.user import User
from app.schemas.site_setting import SiteBrandingResponse, SiteBrandingUpdate
from app.services.storage import is_storage_configured, get_image_url

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/site-config", tags=["site-config"])


def extract_object_key_from_url(url: str | None) -> str | None:
    """
    Extract the object key from a storage URL.
    Handles both direct URLs (https://bucket.../key) and proxy URLs (/api/image-proxy/key)
    """
    if not url:
        return None
    
    # If it's a proxy URL, extract the key directly
    if url.startswith("/api/image-proxy/"):
        from urllib.parse import unquote
        return unquote(url.replace("/api/image-proxy/", ""))
    
    # Try to extract from various URL formats
    # For t3.storageapi.dev URLs: https://t3.storageapi.dev/bucket-name/branding/uuid.png
    parsed = urlparse(url)
    path = parsed.path.lstrip("/")
    
    # Try to find common patterns
    # Pattern 1: /bucket-name/folder/filename or /bucket/folder/filename
    parts = path.split("/")
    if len(parts) >= 3:
        # Assume format: bucket/folder/filename or account/bucket/folder/filename
        # Try to find 'branding', 'annotators', 'carousel', 'sponsors'
        for i, part in enumerate(parts):
            if part in {"branding", "annotators", "carousel", "sponsors"}:
                # Return everything from this folder onwards
                return "/".join(parts[i:])
    
    # If we can't extract, return None
    logger.warning("Could not extract object key from URL: %s", url)
    return None


def regenerate_image_url(url: str | None) -> str | None:
    """
    Regenerate a working image URL from a stored URL.
    Always returns a working URL (Signed URL or Proxy URL), never the original S3 URL.
    """
    if not url:
        return None
    
    try:
        object_key = extract_object_key_from_url(url)
        if not object_key:
            logger.warning("Could not extract object key from: %s", url)
            # Fallback: if we can't extract, use a generic proxy URL
            # This should not happen with properly formatted URLs
            from urllib.parse import quote
            return f"/api/image-proxy/{quote(url, safe='')}"
        
        if is_storage_configured():
            fresh_url = get_image_url(object_key)
            logger.info("Regenerated URL for %s -> %s", object_key, fresh_url)
            return fresh_url
        else:
            logger.warning("Storage not configured, using proxy URL as fallback")
            from urllib.parse import quote
            return f"/api/image-proxy/{quote(object_key, safe='')}"
    except Exception as exc:
        logger.warning("Error regenerating URL for %s: %s - using proxy URL", url, str(exc))
        # Always ensure we return a proxy URL, never the original S3 URL
        try:
            object_key = extract_object_key_from_url(url)
            if object_key:
                from urllib.parse import quote
                return f"/api/image-proxy/{quote(object_key, safe='')}"
        except:
            pass
        # Last resort: return None rather than broken S3 URL
        return None


@router.get("/branding", response_model=SiteBrandingResponse)
async def get_branding(db: Session = Depends(get_db)):
    items = {
        item.key: item.value
        for item in db.query(SiteSetting).filter(
            SiteSetting.key.in_(["brand_logo_url", "admin_brand_logo_url"])
        ).all()
    }
    
    # Regenerate URLs to ensure they work
    return SiteBrandingResponse(
        brand_logo_url=regenerate_image_url(items.get("brand_logo_url")),
        admin_brand_logo_url=regenerate_image_url(items.get("admin_brand_logo_url")),
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
