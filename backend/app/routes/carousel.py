from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.carousel import Carousel
from app.schemas.carousel import (
    CarouselCreate,
    CarouselUpdate,
    CarouselResponse
)

router = APIRouter(prefix="/api/carousel", tags=["carousel"])


@router.get("/", response_model=list[CarouselResponse])
async def list_carousel_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """List all active carousel items"""
    items = db.query(Carousel).filter(
        Carousel.is_active == True
    ).order_by(Carousel.order).offset(skip).limit(limit).all()
    return items


@router.post("/", response_model=CarouselResponse)
async def create_carousel_item(
    item: CarouselCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Create a new carousel item"""
    db_item = Carousel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/{item_id}", response_model=CarouselResponse)
async def get_carousel_item(item_id: int, db: Session = Depends(get_db)):
    """Get carousel item details"""
    item = db.query(Carousel).filter(Carousel.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carousel item not found"
        )
    return item


@router.put("/{item_id}", response_model=CarouselResponse)
async def update_carousel_item(
    item_id: int,
    item_update: CarouselUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Update carousel item"""
    db_item = db.query(Carousel).filter(Carousel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carousel item not found"
        )
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_carousel_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete carousel item (soft delete)"""
    db_item = db.query(Carousel).filter(Carousel.id == item_id).first()
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carousel item not found"
        )
    
    db_item.is_active = False
    db.add(db_item)
    db.commit()
    return {"message": "Carousel item deleted"}
