from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.sponsorship import Sponsorship
from app.schemas.sponsorship import (
    SponsorshipCreate,
    SponsorshipUpdate,
    SponsorshipResponse
)

router = APIRouter(prefix="/api/sponsorships", tags=["sponsorships"])


@router.get("/", response_model=list[SponsorshipResponse])
async def list_sponsorships(
    position: str = Query("", min_length=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """List all active sponsorships"""
    query = db.query(Sponsorship).filter(Sponsorship.is_active == True)
    
    if position:
        query = query.filter(Sponsorship.position == position)
    
    sponsorships = query.order_by(Sponsorship.order).offset(skip).limit(limit).all()
    return sponsorships


@router.post("/", response_model=SponsorshipResponse)
async def create_sponsorship(
    sponsorship: SponsorshipCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Create a new sponsorship"""
    db_sponsorship = Sponsorship(**sponsorship.dict())
    db.add(db_sponsorship)
    db.commit()
    db.refresh(db_sponsorship)
    return db_sponsorship


@router.get("/{sponsorship_id}", response_model=SponsorshipResponse)
async def get_sponsorship(sponsorship_id: int, db: Session = Depends(get_db)):
    """Get sponsorship details"""
    sponsorship = db.query(Sponsorship).filter(Sponsorship.id == sponsorship_id).first()
    if not sponsorship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsorship not found"
        )
    return sponsorship


@router.put("/{sponsorship_id}", response_model=SponsorshipResponse)
async def update_sponsorship(
    sponsorship_id: int,
    sponsorship_update: SponsorshipUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Update sponsorship"""
    db_sponsorship = db.query(Sponsorship).filter(Sponsorship.id == sponsorship_id).first()
    if not db_sponsorship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsorship not found"
        )
    
    update_data = sponsorship_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sponsorship, field, value)
    
    db.add(db_sponsorship)
    db.commit()
    db.refresh(db_sponsorship)
    return db_sponsorship


@router.delete("/{sponsorship_id}")
async def delete_sponsorship(
    sponsorship_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete sponsorship (soft delete)"""
    db_sponsorship = db.query(Sponsorship).filter(Sponsorship.id == sponsorship_id).first()
    if not db_sponsorship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sponsorship not found"
        )
    
    db_sponsorship.is_active = False
    db.add(db_sponsorship)
    db.commit()
    return {"message": "Sponsorship deleted"}
