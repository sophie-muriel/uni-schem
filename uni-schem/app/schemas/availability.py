from datetime import time
from pydantic import BaseModel
from app.models.day import Day


class AvailabilityBase(BaseModel):
    """
    Shared attributes for professor availability.

    Attributes:
        professor_id (int): The id of the professor.
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


class AvailabilityUpdate(BaseModel):
    """
    Schema for updating availability fields. All fields are optional to allow partial updates.

    Attributes:
        professor_id (Optional[int]): Updated professor ID.
        day (Optional[Day]): Updated day of the week.
        start_time (Optional[time]): Updated start time.
        end_time (Optional[time]): Updated end time.
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
