from datetime import time
from pydantic import BaseModel
from app.models.day import Day


class AvailabilityBase(BaseModel):
    """
    Shared attributes for professor availability.

    Attributes:
        professor_id (int): The ID of the professor.
        day (Day): Day of the week.
        start_time (time): Start time of the availability slot.
        end_time (time): End time of the availability slot.
    """
    professor_id: int
    day: Day
    start_time: time
    end_time: time


class AvailabilityCreate(AvailabilityBase):
    """
    Schema for creating a new availability slot.

    Inherits:
        AvailabilityBase: professor_id, day, start_time, end_time.
    """
    pass


class AvailabilityUpdate(BaseModel):
    """
    Schema for updating availability fields. All fields optional.
    """
    professor_id: int | None = None
    day: Day | None = None
    start_time: time | None = None
    end_time: time | None = None


class AvailabilityOut(AvailabilityBase):
    """
    Schema for returning availability data.

    Adds:
        availability_id (int): Unique identifier for the availability entry.
    """
    availability_id: int

    class Config:
        orm_mode = True
