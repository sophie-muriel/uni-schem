from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityOut,
)
from app.services import availability_service
from app.db.database import SessionLocal

router = APIRouter()


def get_db():
    """
    Provides a SQLAlchemy session to the endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AvailabilityOut)
def create_availability_route(data: AvailabilityCreate, db: Session = Depends(get_db)):
    """
    Create a new professor availability entry.
    """
    try:
        return availability_service.register_availability(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AvailabilityOut])
def list_availabilities_route(db: Session = Depends(get_db)):
    """
    Retrieve all professor availability entries.
    """
    return availability_service.list_availabilities(db)


@router.get("/{availability_id}", response_model=AvailabilityOut)
def get_availability_route(availability_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single availability entry by ID.
    """
    availability = availability_service.get_availability(db, availability_id)
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    return availability


@router.put("/{availability_id}", response_model=AvailabilityOut)
def update_availability_route(
    availability_id: int, updates: AvailabilityUpdate, db: Session = Depends(get_db)
):
    """
    Update a professor's availability.
    """
    updated = availability_service.modify_availability(db, availability_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Availability not found")
    return updated


@router.delete("/{availability_id}")
def delete_availability_route(availability_id: int, db: Session = Depends(get_db)):
    """
    Delete a professor's availability entry by ID.
    """
    if not availability_service.remove_availability(db, availability_id):
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}
