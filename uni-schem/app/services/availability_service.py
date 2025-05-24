from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.availability import Availability
from app.schemas.availability import AvailabilityCreate, AvailabilityUpdate
from app.repositories import availability_repository

def register_availability(db: Session, data: AvailabilityCreate) -> Availability:
    """
    Registers a new availability entry for a professor.

    Args:
        db (Session): SQLAlchemy session.
        data (AvailabilityCreate): Input data for the availability.

    Returns:
        Availability: The newly created availability.
    """
    # Check if availability overlaps with an existing availability
    existing_availability = availability_repository.get_availability_by_professor_and_time(
        db, data.professor_id, data.day, data.start_time, data.end_time
    )
    
    if existing_availability:
        raise ValueError("This professor already has availability at this time.")

    new_availability = Availability(
        professor_id=data.professor_id,
        day=data.day,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    
    return availability_repository.create_availability(db, new_availability)


def get_availability(db: Session, availability_id: int) -> Optional[Availability]:
    """
    Retrieves availability by ID.
    """
    return availability_repository.get_availability_by_id(db, availability_id)


def list_availabilities(db: Session) -> List[Availability]:
    """
    Retrieves all availability entries.
    """
    return availability_repository.get_all_availabilities(db)


def get_availabilities_by_professor_id(db: Session, professor_id: int) -> List[Availability]:
    """
    Retrieves all availability entries for a professor.
    """
    return availability_repository.get_availabilities_by_professor_id(db, professor_id)


def modify_availability(
    db: Session, availability_id: int, updates: AvailabilityUpdate
) -> Optional[Availability]:
    """
    Updates an availability entry.
    """
    return availability_repository.update_availability(
        db, availability_id, updates.dict(exclude_unset=True)
    )


def remove_availability(db: Session, availability_id: int) -> bool:
    """
    Deletes an availability entry.
    """
    return availability_repository.delete_availability(db, availability_id)
