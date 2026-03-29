from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.annotator import Annotator
from app.schemas.annotator import (
    AnnotatorCreate, 
    AnnotatorUpdate, 
    AnnotatorResponse,
    AnnotatorMiniResponse
)

router = APIRouter(prefix="/api/annotators", tags=["annotators"])


@router.get("/", response_model=list[AnnotatorMiniResponse])
async def list_annotators(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query("", min_length=0),
    db: Session = Depends(get_db)
):
    """List all active annotators with optional search"""
    query = db.query(Annotator).filter(Annotator.is_active == True)
    
    if search:
        query = query.filter(
            Annotator.company_name.ilike(f"%{search}%") |
            Annotator.description.ilike(f"%{search}%")
        )
    
    annotators = query.offset(skip).limit(limit).all()
    return annotators


@router.post("/", response_model=AnnotatorResponse)
async def create_annotator(
    annotator: AnnotatorCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Create a new annotator/company"""
    # Check if slug already exists
    existing = db.query(Annotator).filter(Annotator.slug == annotator.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    existing_email = db.query(Annotator).filter(Annotator.email == annotator.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail ja esta vinculado a outra empresa"
        )

    db_annotator = Annotator(**annotator.dict())
    db.add(db_annotator)

    try:
        db.commit()
        db.refresh(db_annotator)
        return db_annotator
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nao foi possivel cadastrar a empresa. Verifique slug e e-mail unicos."
        )


@router.get("/{annotator_id}", response_model=AnnotatorResponse)
async def get_annotator(annotator_id: int, db: Session = Depends(get_db)):
    """Get annotator details"""
    annotator = db.query(Annotator).filter(Annotator.id == annotator_id).first()
    if not annotator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotator not found"
        )
    return annotator


@router.get("/slug/{slug}", response_model=AnnotatorResponse)
async def get_annotator_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get annotator by slug (micro site)"""
    annotator = db.query(Annotator).filter(Annotator.slug == slug).first()
    if not annotator or not annotator.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotator not found"
        )
    return annotator


@router.put("/{annotator_id}", response_model=AnnotatorResponse)
async def update_annotator(
    annotator_id: int,
    annotator_update: AnnotatorUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Update annotator information"""
    db_annotator = db.query(Annotator).filter(Annotator.id == annotator_id).first()
    if not db_annotator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotator not found"
        )
    
    update_data = annotator_update.dict(exclude_unset=True)

    if "slug" in update_data and update_data["slug"]:
        existing_slug = db.query(Annotator).filter(
            Annotator.slug == update_data["slug"],
            Annotator.id != annotator_id
        ).first()
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este slug ja esta em uso por outra empresa"
            )

    if "email" in update_data and update_data["email"]:
        existing_email = db.query(Annotator).filter(
            Annotator.email == update_data["email"],
            Annotator.id != annotator_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail ja esta vinculado a outra empresa"
            )

    for field, value in update_data.items():
        setattr(db_annotator, field, value)
    
    db.add(db_annotator)
    try:
        db.commit()
        db.refresh(db_annotator)
        return db_annotator
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nao foi possivel atualizar a empresa. Verifique slug e e-mail unicos."
        )


@router.delete("/{annotator_id}")
async def delete_annotator(
    annotator_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete annotator (soft delete)"""
    db_annotator = db.query(Annotator).filter(Annotator.id == annotator_id).first()
    if not db_annotator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotator not found"
        )
    
    db_annotator.is_active = False
    db.add(db_annotator)
    db.commit()
    return {"message": "Annotator deleted"}
