from datetime import time
from pydantic import BaseModel
from app.models.day import Day


class ScheduleBase(BaseModel):
    """
    Shared attributes for schedule models.

    Attributes:
        course_id (int): ID of the scheduled course.
        day (Day): Day of the week when the course is scheduled.
        start_time (time): Start time of the session.
        end_time (time): End time of the session.
        classroom_id (int): ID of the classroom assigned to this session.
    """
    course_id: int
    day: Day
    start_time: time
    end_time: time
    classroom_id: int


class ScheduleCreate(ScheduleBase):
    """
    Schema for creating a new schedule entry.

    Inherits:
        course_id, day, start_time, end_time, classroom_id from ScheduleBase.
    """
    pass


class ScheduleUpdate(BaseModel):
    """
    Schema for updating schedule data. All fields are optional.

    Attributes:
        course_id (Optional[int]): Updated course ID.
        day (Optional[Day]): Updated day of the week.
        start_time (Optional[time]): Updated start time.
        end_time (Optional[time]): Updated end time.
        classroom_id (Optional[int]): Updated classroom ID.
    """
    course_id: int | None = None
    day: Day | None = None
    start_time: time | None = None
    end_time: time | None = None
    classroom_id: int | None = None


class ScheduleOut(ScheduleBase):
    """
    Schema used for returning schedule data in API responses.

    Adds:
        schedule_id (int): Unique identifier for the schedule entry.
    """
    schedule_id: int

    class Config:
        orm_mode = True
