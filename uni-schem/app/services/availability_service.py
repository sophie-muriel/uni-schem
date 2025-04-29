from sqlalchemy.orm import Session
from typing import List, Optional
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

    Raises:
        ValueError: If an entry with the same ID already exists.
    """
    existing = availability_repository.get_availability_by_id(db, data.availability_id)
    if existing:
        raise ValueError("Availability with this ID already exists.")

    new_availability = Availability(**data.dict())
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


def modify_availability(
    db: Session, availability_id: int, updates: AvailabilityUpdate
) -> Optional[Availability]:
    """
    Updates an availability entry.

    Args:
        db (Session): SQLAlchemy session.
        availability_id (int): ID of the availability to update.
        updates (AvailabilityUpdate): Data to update.

    Returns:
        Optional[Availability]: Updated record or None if not found.
    """
    return availability_repository.update_availability(
        db, availability_id, updates.dict(exclude_unset=True)
    )


def remove_availability(db: Session, availability_id: int) -> bool:
    """
    Deletes an availability entry.

    Args:
        db (Session): SQLAlchemy session.
        availability_id (int): ID of the availability to delete.

    Returns:
        bool: True if deleted, False otherwise.
    """
    return availability_repository.delete_availability(db, availability_id)
