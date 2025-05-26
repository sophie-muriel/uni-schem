from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.models.course import Course
from app.models.classroom import Classroom
from fastapi import HTTPException, status


def create_schedule(db: Session, schedule: Schedule) -> Schedule:
    """
    Inserts a new schedule entry into the database after validating course and classroom existence,
    and checking for conflicts in the timetable.

    Args:
        db (Session): SQLAlchemy session.
        schedule (Schedule): The schedule to create.

    Returns:
        Schedule: The newly created schedule.

    Raises:
        HTTPException: If the course or classroom does not exist or if the schedule overlaps with an existing schedule.
    """
    course = db.query(Course).filter(Course.course_id == schedule.course_id).first()
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    classroom = db.query(Classroom).filter(Classroom.classroom_id == schedule.classroom_id).first()
    if not classroom:
        raise HTTPException(
            status_code=404,
            detail="Classroom not found"
        )

    existing_schedule_for_course = db.query(Schedule).filter(
        Schedule.course_id == schedule.course_id,
        Schedule.day == schedule.day,
        Schedule.start_time == schedule.start_time,
        Schedule.end_time == schedule.end_time
    ).first()

    if existing_schedule_for_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is already scheduled at the same time."
        )

    existing_schedule_in_classroom = db.query(Schedule).filter(
        Schedule.classroom_id == schedule.classroom_id,
        Schedule.day == schedule.day,
        Schedule.start_time == schedule.start_time,
        Schedule.end_time == schedule.end_time
    ).first()

    if existing_schedule_in_classroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Classroom is already booked at this time."
        )

    db.add(schedule)
    db.flush()
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
    Deletes a schedule from the system by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        schedule_id (int): The ID of the schedule to delete.

    Returns:
        bool: True if the schedule was successfully deleted, False otherwise.
    """
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return False

    if schedule.course:
        db.delete(schedule.course)
    if schedule.classroom:
        schedule.classroom_id = None

    db.delete(schedule)
    db.commit()
    return True
