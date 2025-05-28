from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.availability import Availability
from app.schemas.availability import AvailabilityCreate, AvailabilityUpdate
from app.repositories import availability_repository, professor_repository
from app.models.professor import Professor


def register_availability(db: Session, data: AvailabilityCreate) -> Availability:
    """
    Registers a new availability entry for a professor.

    Args:
        db (Session): SQLAlchemy session.
        data (AvailabilityCreate): Input data for the availability.

    Returns:
        Availability: The newly created availability.
    """
    professor = professor_repository.get_professor_by_id(db, data.professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    existing_availability = availability_repository.get_availability_by_professor_and_time(
        db, data.professor_id, data.day, data.start_time, data.end_time
    )
    if existing_availability:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This professor already has availability at this time."
        )

    new_availability = Availability(
        professor_id=data.professor_id,
        day=data.day,
        start_time=data.start_time,
        end_time=data.end_time,
    )

    return availability_repository.create_availability(db, new_availability)


def get_availability(db: Session, availability_id: int) -> Optional[Availability]:
    """
    Retrieves a specific availability by its ID.

    Args:
        db (Session): Database session.
        availability_id (int): The ID of the availability entry.

    Returns:
        Optional[Availability]: The availability if found, otherwise None.
    """
    return availability_repository.get_availability_by_id(db, availability_id)


def list_availabilities(db: Session) -> List[Availability]:
    """
    Retrieves all availability entries in the system.

    Args:
        db (Session): Database session.

    Returns:
        List[Availability]: List containing all availability records.
    """
    return availability_repository.get_all_availabilities(db)


def modify_availability(
    db: Session, availability_id: int, updates: AvailabilityUpdate
) -> Optional[Availability]:
    """
    Updates an existing availability entry with the provided fields.

    Args:
        db (Session): Database session.
        availability_id (int): ID of the availability to update.
        updates (AvailabilityUpdate): Fields to update in the availability.

    Returns:
        Optional[Availability]: The updated availability entry, or None if not found.
    """
    if updates.professor_id:
        professor = professor_repository.get_professor_by_id(db, updates.professor_id)
        if not professor:
            raise HTTPException(status_code=404, detail="Professor not found")

    return availability_repository.update_availability(
        db, availability_id, updates.dict(exclude_unset=True)
    )


def remove_availability(db: Session, availability_id: int) -> bool:
    """
    Deletes an availability entry by its ID.

    Args:
        db (Session): Database session.
        availability_id (int): ID of the availability to delete.

    Returns:
        bool: True if deletion was successful, False if not found.
    """
    return availability_repository.delete_availability(db, availability_id)
