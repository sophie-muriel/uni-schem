from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.repositories import schedule_repository


def register_schedule(db: Session, data: ScheduleCreate) -> Schedule:
    """
    Registers a new schedule in the system.

    Args:
        db (Session): SQLAlchemy session.
        data (ScheduleCreate): Input data for the new schedule.

    Returns:
        Schedule: The created schedule.
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
    Retrieves a schedule by its ID.
    """
    return schedule_repository.get_schedule_by_id(db, schedule_id)


def list_schedules(db: Session) -> List[Schedule]:
    """
    Retrieves all schedules from the database.
    """
    return schedule_repository.get_all_schedules(db)


def modify_schedule(
    db: Session, schedule_id: int, updates: ScheduleUpdate
) -> Optional[Schedule]:
    """
    Updates an existing schedule with new data.
    """
    return schedule_repository.update_schedule(
        db, schedule_id, updates.dict(exclude_unset=True)
    )


def remove_schedule(db: Session, schedule_id: int) -> bool:
    """
    Deletes a schedule from the system.
    """
    return schedule_repository.delete_schedule(db, schedule_id)
