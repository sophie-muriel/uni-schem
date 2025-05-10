
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
    Create a new schedule entry.
    """
    try:
        return schedule_service.register_schedule(db, schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[ScheduleOut])
def list_schedules_route(db: Session = Depends(get_db)):
    """
    Retrieve all schedules.
    """
    return schedule_service.list_schedules(db)


@router.get("/{schedule_id}", response_model=ScheduleOut)
def get_schedule_route(schedule_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a schedule by its ID.
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
    Update an existing schedule entry.
    """
    updated = schedule_service.modify_schedule(db, schedule_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return updated


@router.delete("/{schedule_id}")
def delete_schedule_route(schedule_id: int, db: Session = Depends(get_db)):
    """
    Delete a schedule by ID.
    """
    if not schedule_service.remove_schedule(db, schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}
