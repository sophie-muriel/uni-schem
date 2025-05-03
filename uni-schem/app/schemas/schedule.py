from datetime import time
from pydantic import BaseModel
from app.models.day import Day


class ScheduleBase(BaseModel):
    """
    Shared attributes for schedule models.
    """

    course_id: int
    day: Day
    start_time: time
    end_time: time
    classroom_id: int


class ScheduleCreate(ScheduleBase):
    """
    Schema for creating a new schedule.
    """

    schedule_id: int


class ScheduleUpdate(BaseModel):
    """
    Schema for updating schedule data. All fields optional.
    """

    course_id: int | None = None
    day: Day | None = None
    start_time: time | None = None
    end_time: time | None = None
    classroom_id: int | None = None


class ScheduleOut(ScheduleBase):
    """
    Schema used for returning schedule data in API responses.
    """

    schedule_id: int

    class Config:
        orm_mode = True
