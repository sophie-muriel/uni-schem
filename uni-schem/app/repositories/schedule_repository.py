from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.schedule import Schedule


def create_schedule(db: Session, schedule: Schedule) -> Schedule:
    """
    Adds a new schedule to the database.

    Args:
        db (Session): SQLAlchemy session object.
        schedule (Schedule): The schedule instance to insert.

    Returns:
        Schedule: The newly created schedule.
    """
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def get_schedule_by_id(db: Session, schedule_id: int) -> Optional[Schedule]:
    """
    Retrieves a schedule by its unique ID.

    Args:
        db (Session): SQLAlchemy session object.
        schedule_id (int): The ID of the schedule to retrieve.

    Returns:
        Optional[Schedule]: The schedule if found, else None.
    """
    return db.query(Schedule).filter(Schedule.schedule_id == schedule_id).first()


def get_all_schedules(db: Session) -> List[Schedule]:
    """
    Retrieves all schedules from the database.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[Schedule]: A list of all schedules.
    """
    return db.query(Schedule).all()


def update_schedule(db: Session, schedule_id: int, updates: dict) -> Optional[Schedule]:
    """
    Updates an existing schedule.

    Args:
        db (Session): SQLAlchemy session object.
        schedule_id (int): ID of the schedule to update.
        updates (dict): Fields to be updated.

    Returns:
        Optional[Schedule]: The updated schedule, or None if not found.
    """
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None

    for key, value in updates.items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule


def delete_schedule(db: Session, schedule_id: int) -> bool:
    """
    Deletes a schedule by ID.

    Args:
        db (Session): SQLAlchemy session object.
        schedule_id (int): ID of the schedule to delete.

    Returns:
        bool: True if deleted, False otherwise.
    """
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return False

    db.delete(schedule)
    db.commit()
    return True
