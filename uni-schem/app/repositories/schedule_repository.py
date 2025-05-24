from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from fastapi import HTTPException, status


def create_schedule(db: Session, schedule: Schedule) -> Schedule:
    """
    Inserts a new schedule entry into the database after validating no overlap.

    Args:
        db (Session): SQLAlchemy session.
        schedule (Schedule): The schedule to create.

    Returns:
        Schedule: The newly created schedule.

    Raises:
        HTTPException: If the schedule overlaps with an existing schedule.
    """
    existing_schedule = db.query(Schedule).filter(
        Schedule.course_id == schedule.course_id,
        Schedule.classroom_id == schedule.classroom_id,
        Schedule.day == schedule.day,
        Schedule.start_time == schedule.start_time,
        Schedule.end_time == schedule.end_time
    ).first()

    if existing_schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The schedule already exists for this course and classroom in the same timetable."
        )
    try:
        db.add(schedule)
        db.flush()
        db.commit()
        db.refresh(schedule)
        return schedule
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the timetable."
        )


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


def get_schedules_by_course_id(db: Session, course_id: int) -> List[Schedule]:
    """
    Retrieves all schedules for a specific course by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        course_id (int): The ID of the course.

    Returns:
        List[Schedule]: A list of schedules for the specified course.
    """
    return db.query(Schedule).filter(Schedule.course_id == course_id).all()


def get_schedules_by_classroom_id(db: Session, classroom_id: int) -> List[Schedule]:
    """
    Retrieves all schedules for a specific classroom by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        classroom_id (int): The ID of the classroom.

    Returns:
        List[Schedule]: A list of schedules for the specified classroom.
    """
    return db.query(Schedule).filter(Schedule.classroom_id == classroom_id).all()


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
