from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.availability import Availability


def create_availability(db: Session, availability: Availability) -> Availability:
    """
    Inserts a new availability entry into the database.

    Args:
        db (Session): SQLAlchemy session.
        availability (Availability): The availability to create.

    Returns:
        Availability: The newly created availability.
    """
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


def get_availability_by_id(db: Session, availability_id: int) -> Optional[Availability]:
    """
    Retrieves availability by its ID.

    Args:
        db (Session): SQLAlchemy session.
        availability_id (int): The ID of the availability.

    Returns:
        Optional[Availability]: The availability if found, else None.
    """
    return (
        db.query(Availability)
        .filter(Availability.availability_id == availability_id)
        .first()
    )


def get_all_availabilities(db: Session) -> List[Availability]:
    """
    Retrieves all availability entries.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Availability]: A list of all availability records.
    """
    return db.query(Availability).all()


def update_availability(
    db: Session, availability_id: int, updates: dict
) -> Optional[Availability]:
    """
    Updates an availability entry.

    Args:
        db (Session): SQLAlchemy session.
        availability_id (int): ID of the availability to update.
        updates (dict): Fields to update.

    Returns:
        Optional[Availability]: The updated availability, or None if not found.
    """
    availability = get_availability_by_id(db, availability_id)
    if not availability:
        return None

    for key, value in updates.items():
        setattr(availability, key, value)

    db.commit()
    db.refresh(availability)
    return availability


def delete_availability(db: Session, availability_id: int) -> bool:
    """
    Deletes an availability entry by its ID.

    Args:
        db (Session): SQLAlchemy session.
        availability_id (int): The ID of the availability.

    Returns:
        bool: True if deleted, False if not found.
    """
    availability = get_availability_by_id(db, availability_id)
    if not availability:
        return False

    db.delete(availability)
    db.commit()
    return True
