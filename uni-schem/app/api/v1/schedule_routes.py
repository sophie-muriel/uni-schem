from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleOut
from app.services import schedule_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=ScheduleOut)
def create_schedule_route(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    """
    Creates a new schedule entry after checking if the course and classroom exist and if the schedule doesn't overlap.

    Args:
        schedule (ScheduleCreate): The schedule data to be registered.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ScheduleOut: The newly created schedule record.

    Raises:
        HTTPException: If a course_id or classroom_id doesn't exist or the schedule overlaps, returns a 404 Not Found
        with the corresponding error message.
    """
    try:
        return schedule_service.register_schedule(db, schedule)
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during schedule creation.")


@router.get("/", response_model=List[ScheduleOut])
def list_schedules_route(db: Session = Depends(get_db)):
    """
    Retrieves all schedule entries.

    Args:
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[ScheduleOut]: A list of all schedules.
    """
    return schedule_service.list_schedules(db)


@router.get("/{schedule_id}", response_model=ScheduleOut)
def get_schedule_route(schedule_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a schedule entry by its unique ID.

    Args:
        schedule_id (int): The unique identifier of the schedule.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ScheduleOut: The requested schedule record.

    Raises:
        HTTPException: If the schedule is not found, returns a 404 Not Found error.
    """
    schedule = schedule_service.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@router.get("/course/{course_id}", response_model=List[ScheduleOut])
def get_schedules_by_course_id_route(course_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all schedules for a specific course by its ID.

    Args:
        course_id (int): The unique identifier of the course.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[ScheduleOut]: A list of schedules for the specified course.

    Raises:
        HTTPException: If no schedules are found for the course, returns a 404 Not Found error.
    """
    schedules = schedule_service.get_schedules_by_course_id(db, course_id)
    if not schedules:
        raise HTTPException(
            status_code=404, detail="No schedules found for this course")
    return schedules


@router.get("/classroom/{classroom_id}", response_model=List[ScheduleOut])
def get_schedules_by_classroom_id_route(classroom_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all schedules for a specific classroom by its ID.

    Args:
        classroom_id (int): The unique identifier of the classroom.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[ScheduleOut]: A list of schedules for the specified classroom.

    Raises:
        HTTPException: If no schedules are found for the classroom, returns a 404 Not Found error.
    """
    schedules = schedule_service.get_schedules_by_classroom_id(db, classroom_id)
    if not schedules:
        raise HTTPException(
            status_code=404, detail="No schedules found for this classroom")
    return schedules


@router.put("/{schedule_id}", response_model=ScheduleOut)
def update_schedule_route(schedule_id: int, updates: ScheduleUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing schedule entry by its ID.

    Args:
        schedule_id (int): The unique identifier of the schedule to update.
        updates (ScheduleUpdate): The new values to apply to the schedule.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ScheduleOut: The updated schedule record.

    Raises:
        HTTPException: If the schedule is not found, returns a 404 Not Found error.
    """
    updated = schedule_service.modify_schedule(db, schedule_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return updated


@router.delete("/{schedule_id}")
def delete_schedule_route(schedule_id: int, db: Session = Depends(get_db)):
    """
    Deletes a schedule entry by its ID.

    Args:
        schedule_id (int): The unique identifier of the schedule to delete.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the schedule is not found, returns a 404 Not Found error.
    """
    if not schedule_service.remove_schedule(db, schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}
