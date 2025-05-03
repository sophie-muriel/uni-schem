from datetime import time
from pydantic import BaseModel
from app.models.day import Day


class AvailabilityBase(BaseModel):
    """
    Shared attributes for professor availability.
    """

    professor_id: int
    day: Day
    start_time: time
    end_time: time


class AvailabilityCreate(AvailabilityBase):
    """
    Schema for creating a new availability slot.
    """

    availability_id: int


class AvailabilityUpdate(BaseModel):
    """
    Schema for updating availability fields. All optional.
    """

    professor_id: int | None = None
    day: Day | None = None
    start_time: time | None = None
    end_time: time | None = None


class AvailabilityOut(AvailabilityBase):
    """
    Schema for returning availability data.
    """

    availability_id: int

    class Config:
        orm_mode = True
