from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.repositories import schedule_repository


def register_schedule(db: Session, data: ScheduleCreate) -> Schedule:
    """
    Registers a new schedule in the system.

    Args:
        db (Session): SQLAlchemy session for interacting with the database.
        data (ScheduleCreate): Input data containing course ID, day, start time, end time, and classroom ID.

    Returns:
        Schedule: The newly created schedule.
    """
    new_schedule = Schedule(
        course_id=data.course_id,
        day=data.day,
        start_time=data.start_time,
        end_time=data.end_time,
        classroom_id=data.classroom_id,
    )
    return schedule_repository.create_schedule(db, new_schedule)


def get_schedule(db: Session, schedule_id: int) -> Optional[Schedule]:
    """
    Retrieves a schedule by its unique ID.

    Args:
        db (Session): SQLAlchemy session.
        schedule_id (int): The ID of the schedule to retrieve.

    Returns:
        Optional[Schedule]: The schedule if found, otherwise None.
    """
    return schedule_repository.get_schedule_by_id(db, schedule_id)


def list_schedules(db: Session) -> List[Schedule]:
    """
    Retrieves all schedules stored in the system.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Schedule]: A list of all schedules.
    """
    return schedule_repository.get_all_schedules(db)


def modify_schedule(
    db: Session, schedule_id: int, updates: ScheduleUpdate
) -> Optional[Schedule]:
    """
    Updates an existing schedule's details.

    Args:
        db (Session): SQLAlchemy session.
        schedule_id (int): The ID of the schedule to update.
        updates (ScheduleUpdate): Fields to update in the schedule.

    Returns:
        Optional[Schedule]: The updated schedule if found and modified, else None.
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
        bool: True if the schedule was successfully deleted, False otherwise.
    """
    return schedule_repository.delete_schedule(db, schedule_id)


def get_schedules_by_course_id(db: Session, course_id: int) -> List[Schedule]:
    """
    Retrieves all schedules for a specific course by its ID.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): The ID of the course.

    Returns:
        List[Schedule]: A list of schedules for the specified course.
    """
    return schedule_repository.get_schedules_by_course_id(db, course_id)


def get_schedules_by_classroom_id(db: Session, classroom_id: int) -> List[Schedule]:
    """
    Retrieves all schedules for a specific classroom by its ID.

    Args:
        db (Session): SQLAlchemy session.
        classroom_id (int): The ID of the classroom.

    Returns:
        List[Schedule]: A list of schedules for the specified classroom.
    """
    return schedule_repository.get_schedules_by_classroom_id(db, classroom_id)
