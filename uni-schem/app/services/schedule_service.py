from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.repositories import schedule_repository


def register_schedule(db: Session, schedule_data: ScheduleCreate) -> Schedule:
    """
    Registers a new schedule in the system.

    Args:
        db (Session): SQLAlchemy session.
        schedule_data (ScheduleCreate): Input data for the new schedule.

    Returns:
        Schedule: The created schedule.

    Raises:
        ValueError: If a schedule with the same ID already exists.
    """
    existing = schedule_repository.get_schedule_by_id(db, schedule_data.schedule_id)
    if existing:
        raise ValueError("Schedule with this ID already exists.")

    new_schedule = Schedule(**schedule_data.dict())
    return schedule_repository.create_schedule(db, new_schedule)


def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    """
    Retrieves a schedule by its ID.

    Args:
        db (Session): SQLAlchemy session.
        schedule_id (int): The unique ID of the schedule.

    Returns:
        Optional[Schedule]: The found schedule or None.
    """
    return schedule_repository.get_schedule_by_id(db, schedule_id)


def list_schedules(db: Session) -> List[Schedule]:
    """
    Retrieves all schedules from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Schedule]: List of all schedules.
    """
    return schedule_repository.get_all_schedules(db)


def modify_schedule(
    db: Session, schedule_id: int, updates: ScheduleUpdate
) -> Optional[Schedule]:
    """
    Updates an existing schedule with new data.

    Args:
        db (Session): SQLAlchemy session.
        schedule_id (int): The ID of the schedule to update.
        updates (ScheduleUpdate): The updated fields.

    Returns:
        Optional[Schedule]: The updated schedule or None if not found.
    """
    return schedule_repository.update_schedule(
        db, schedule_id, updates.dict(exclude_unset=True)
    )


def remove_schedule(db: Session, schedule_id: int) -> bool:
    """
    Deletes a schedule from the system.

    Args:
        db (Session): SQLAlchemy session.
        schedule_id (int): The ID of the schedule to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    return schedule_repository.delete_schedule(db, schedule_id)
