from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.security import get_current_admin
from app.database.database import get_db
from app.models.annotator import Annotator
from app.models.carousel import Carousel
from app.models.job import Job
from app.models.sponsorship import Sponsorship
from app.models.user import User
from app.schemas.annotator import AnnotatorResponse
from app.schemas.carousel import CarouselResponse
from app.schemas.job import JobResponse
from app.schemas.sponsorship import SponsorshipResponse
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

UPLOADS_ROOT = Path(__file__).resolve().parents[2] / "uploads"
ALLOWED_UPLOAD_FOLDERS = {"annotators", "carousel", "sponsors"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@router.get("/me", response_model=UserResponse)
async def admin_me(current_admin: User = Depends(get_current_admin)):
    """Return the authenticated admin."""
    return current_admin


@router.post("/upload-image", response_model=dict)
async def admin_upload_image(
    request: Request,
    folder: str = Query("annotators"),
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin),
):
    """Upload an admin-managed image and return its public URL."""
    if folder not in ALLOWED_UPLOAD_FOLDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid upload folder"
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file selected"
        )

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported image format. Use JPG, PNG, WEBP or GIF."
        )

    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be an image"
        )

    target_dir = UPLOADS_ROOT / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{extension}"
    target_path = target_dir / filename
    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file"
        )

    target_path.write_bytes(contents)
    public_path = f"/uploads/{folder}/{filename}"
    public_url = str(request.base_url).rstrip("/") + public_path

    return {
        "filename": filename,
        "path": public_path,
        "url": public_url,
        "uploaded_by": current_admin.email,
    }


@router.get("/dashboard", response_model=dict)
async def admin_dashboard(db: Session = Depends(get_db)):
    """Return dashboard counters."""
    return {
        "annotators_total": db.query(Annotator).count(),
        "annotators_active": db.query(Annotator).filter(Annotator.is_active == True).count(),
        "jobs_total": db.query(Job).count(),
        "jobs_active": db.query(Job).filter(Job.is_active == True).count(),
        "carousel_total": db.query(Carousel).count(),
        "carousel_active": db.query(Carousel).filter(Carousel.is_active == True).count(),
        "sponsorships_total": db.query(Sponsorship).count(),
        "sponsorships_active": db.query(Sponsorship).filter(Sponsorship.is_active == True).count(),
    }


@router.get("/annotators", response_model=list[AnnotatorResponse])
async def admin_list_annotators(
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Annotator).order_by(Annotator.id.desc())
    if active_only:
        query = query.filter(Annotator.is_active == True)
    return query.all()


@router.get("/jobs", response_model=list[JobResponse])
async def admin_list_jobs(
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Job).order_by(Job.id.desc())
    if active_only:
        query = query.filter(Job.is_active == True)
    return query.all()


@router.get("/carousel", response_model=list[CarouselResponse])
async def admin_list_carousel(
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Carousel).order_by(Carousel.order, Carousel.id.desc())
    if active_only:
        query = query.filter(Carousel.is_active == True)
    return query.all()


@router.get("/sponsorships", response_model=list[SponsorshipResponse])
async def admin_list_sponsorships(
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Sponsorship).order_by(Sponsorship.order, Sponsorship.id.desc())
    if active_only:
        query = query.filter(Sponsorship.is_active == True)
    return query.all()
