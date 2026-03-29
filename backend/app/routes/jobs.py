from email.message import EmailMessage

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.job import Job
from app.services.email import send_email_message
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobMiniResponse
)

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

ALLOWED_RESUME_EXTENSIONS = {".pdf", ".doc", ".docx"}
DOC_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.get("/", response_model=list[JobMiniResponse])
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query("", min_length=0),
    category: str = Query("", min_length=0),
    city: str = Query("", min_length=0),
    featured_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List all active jobs with filtering options"""
    query = db.query(Job).filter(Job.is_active == True)
    
    # Filter by search term
    if search:
        query = query.filter(
            Job.title.ilike(f"%{search}%") |
            Job.description.ilike(f"%{search}%") |
            Job.company_name.ilike(f"%{search}%")
        )
    
    # Filter by category
    if category:
        query = query.filter(Job.category == category)
    
    # Filter by city
    if city:
        query = query.filter(Job.city.ilike(f"%{city}%"))
    
    # Filter by featured
    if featured_only:
        query = query.filter(Job.is_featured == True)
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.post("/", response_model=JobResponse)
async def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    """Create a new job posting"""
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job details"""
    job = db.query(Job).filter(Job.id == job_id, Job.is_active == True).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.post("/{job_id}/apply", response_model=dict)
async def apply_to_job(
    job_id: int,
    applicant_name: str = Form(...),
    applicant_email: str = Form(...),
    applicant_phone: str = Form(""),
    message: str = Form(""),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Apply to a job and send the resume to the company by email."""
    job = db.query(Job).filter(Job.id == job_id, Job.is_active == True).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if not resume.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Selecione um curriculo para enviar."
        )

    extension = ""
    if "." in resume.filename:
        extension = f".{resume.filename.rsplit('.', 1)[-1].lower()}"

    if extension not in ALLOWED_RESUME_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de curriculo invalido. Envie PDF, DOC ou DOCX."
        )

    if resume.content_type and resume.content_type not in DOC_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de arquivo nao suportado para curriculo."
        )

    resume_bytes = await resume.read()
    if not resume_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado esta vazio."
        )

    max_bytes = settings.job_application_max_resume_size_mb * 1024 * 1024
    if len(resume_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O curriculo excede o limite de {settings.job_application_max_resume_size_mb} MB."
        )

    recipient_email = job.contact_email or job.company_email
    email_body = "\n".join([
        "Nova candidatura recebida pelo ShoppingHub.",
        "",
        f"Vaga: {job.title}",
        f"Empresa: {job.company_name}",
        "",
        f"Candidato: {applicant_name}",
        f"E-mail: {applicant_email}",
        f"Telefone: {applicant_phone or 'Nao informado'}",
        "",
        "Mensagem do candidato:",
        message.strip() or "Nenhuma mensagem adicional enviada.",
    ])

    email_message = EmailMessage()
    email_message["Subject"] = f"Nova candidatura para {job.title}"
    email_message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    email_message["To"] = recipient_email
    email_message["Reply-To"] = applicant_email
    email_message.set_content(email_body)
    email_message.add_attachment(
        resume_bytes,
        maintype="application",
        subtype="octet-stream",
        filename=resume.filename,
    )

    try:
        send_email_message(email_message)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Nao foi possivel enviar a candidatura por e-mail."
        ) from exc

    return {
        "message": "Candidatura enviada com sucesso.",
        "job_id": job.id,
        "sent_to": recipient_email,
    }


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Update job posting"""
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete job posting (soft delete)"""
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    db_job.is_active = False
    db.add(db_job)
    db.commit()
    return {"message": "Job deleted"}


@router.get("/company/{company_id}", response_model=list[JobMiniResponse])
async def get_company_jobs(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all jobs for a specific company"""
    jobs = db.query(Job).filter(
        Job.company_id == company_id,
        Job.is_active == True
    ).offset(skip).limit(limit).all()
    return jobs
