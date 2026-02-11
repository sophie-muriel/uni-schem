from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityOut,
)
from app.services import availability_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=AvailabilityOut)
def create_availability_route(data: AvailabilityCreate, db: Session = Depends(get_db)):
    """
    Creates a new availability entry for a professor after checking if the professor exists
    and if the availability does not overlap with others.

    Args:
        data (AvailabilityCreate): The availability information to be registered.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        AvailabilityOut: The newly created availability record.

    Raises:
        HTTPException: If validation fails, raises 400 Bad Request with the error message.
    """
    try:
        return availability_service.register_availability(db, data)
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred during availability creation.")


@router.get("/", response_model=List[AvailabilityOut])
def list_availabilities_route(db: Session = Depends(get_db)):
    """
    Retrieves all professor availability entries from the database.

    Args:
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[AvailabilityOut]: A list of all registered availability records.
    """
    return availability_service.list_availabilities(db)


@router.get("/{availability_id}", response_model=AvailabilityOut)
def get_availability_route(availability_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single availability entry by its ID.

    Args:
        availability_id (int): The unique identifier of the availability entry.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        AvailabilityOut: The requested availability record.

    Raises:
        HTTPException: If the availability entry is not found, returns a 404 Not Found error.
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
    Updates a professor's availability entry by its ID.

    Args:
        availability_id (int): The unique identifier of the availability entry to update.
        updates (AvailabilityUpdate): The data containing the fields to be updated.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        AvailabilityOut: The updated availability record.

    Raises:
        HTTPException: If the availability entry is not found, returns a 404 Not Found error.
    """
    updated = availability_service.modify_availability(
        db, availability_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Availability not found")
    return updated


@router.delete("/{availability_id}")
def delete_availability_route(availability_id: int, db: Session = Depends(get_db)):
    """
    Deletes a professor's availability entry by its ID. The professor associated with the availability
    will also have their associated availabilities deleted in cascade.

    Args:
        availability_id (int): The unique identifier of the availability entry to delete.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        dict: A message confirming successful deletion.

    Raises:
        HTTPException: If the availability entry is not found, returns a 404 Not Found error.
    """
    if not availability_service.remove_availability(db, availability_id):
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}


@router.get("/professor/{professor_id}", response_model=List[AvailabilityOut])
def get_availabilities_by_professor_route(
    professor_id: int, db: Session = Depends(get_db)
):
    """
    Retrieves all availability entries for a given professor.

    Args:
        professor_id (int): The ID of the professor.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[AvailabilityOut]: A list of availability records for the professor.
    """
    availabilities = availability_service.get_availabilities_by_professor_id(
        db, professor_id)
    if not availabilities:
        raise HTTPException(
            status_code=404, detail="No availabilities found for this professor")
    return availabilities
