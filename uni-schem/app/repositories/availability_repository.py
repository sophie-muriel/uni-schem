from typing import List, Optional
from datetime import time
from sqlalchemy.orm import Session
from app.models.availability import Availability
from fastapi import HTTPException, status


def create_availability(db: Session, availability: Availability) -> Availability:
    """
    Inserts a new availability entry into the database after validating no overlap.

    Args:
        db (Session): SQLAlchemy session.
        availability (Availability): The availability to create.

    Returns:
        Availability: The newly created availability.

    Raises:
        HTTPException: If the availability overlaps with an existing availability.
    """
    existing_availability = get_availability_by_professor_and_time(
        db, availability.professor_id, availability.day, availability.start_time,
        availability.end_time
    )

    if existing_availability:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La disponibilidad se solapa con una disponibilidad existente."
        )

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
    return db.query(Availability).filter(Availability.availability_id == availability_id).first()


def get_all_availabilities(db: Session) -> List[Availability]:
    """
    Retrieves all availability entries.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Availability]: A list of all availability records.
    """
    return db.query(Availability).all()


def get_availability_by_professor_and_time(
    db: Session, professor_id: int, day: str, start_time: time, end_time: time
) -> Optional[Availability]:
    """
    Verifies if there is any availability entry that overlaps with the new one for the same
    professor.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): ID of the professor.
        day (str): The day of the week.
        start_time (time): The start time of the availability slot.
        end_time (time): The end time of the availability slot.

    Returns:
        Optional[Availability]: The availability entry if found, else None.
    """
    return db.query(Availability).filter(
        Availability.professor_id == professor_id,
        Availability.day == day,
        # The start time of the new availability should be before the existing end time
        Availability.start_time < end_time,
        # The end time of the new availability should be after the existing start time
        Availability.end_time > start_time
    ).first()


def get_availabilities_by_professor_id(db: Session, professor_id: int) -> List[Availability]:
    """
    Retrieves all availability entries for a professor by their professor_id.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): The ID of the professor.

    Returns:
        List[Availability]: A list of all availability records for the professor.
    """
    return db.query(Availability).filter(Availability.professor_id == professor_id).all()


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

    # Update the fields with the new data
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
