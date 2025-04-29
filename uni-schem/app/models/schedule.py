from pydantic import BaseModel
from datetime import time
from .day import Day


class Schedule(BaseModel):
    """
    Represents the schedule for a course in a specific classroom.

    Attributes:
        schedule_id (int): Unique identifier for the schedule.
        course_id (int): ID of the course this schedule belongs to.
        day (Day): Day of the week.
        start_time (time): Start time of the session.
        end_time (time): End time of the session.
        classroom_id (int): ID of the classroom assigned.
    """

    schedule_id: int
    course_id: int
    day: Day
    start_time: time
    end_time: time
    classroom_id: int
