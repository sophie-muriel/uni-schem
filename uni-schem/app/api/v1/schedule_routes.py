
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
    Creates a new schedule entry.

    Args:
        schedule (ScheduleCreate): The schedule data to be registered.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ScheduleOut: The newly created schedule record.

    Raises:
        HTTPException: If a ValueError occurs during registration, returns a 400 Bad Request
        with the error message.
    """
    try:
        return schedule_service.register_schedule(db, schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


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


@router.put("/{schedule_id}", response_model=ScheduleOut)
def update_schedule_route(
    schedule_id: int, updates: ScheduleUpdate, db: Session = Depends(get_db)
):
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
