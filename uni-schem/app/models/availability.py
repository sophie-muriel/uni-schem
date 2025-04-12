from pydantic import BaseModel
from datetime import time
from .day import Day

class Availability(BaseModel):
    """
    Represents a professor's availability.

    Attributes:
        availability_id (int): Unique identifier for the availability entry.
        professor_id (int): ID of the professor.
        day (Day): Day of the week (Enum).
        start_time (time): Start of availability.
        end_time (time): End of availability.
    """
    availability_id: int
    professor_id: int
    day: Day
    start_time: time
    end_time: time