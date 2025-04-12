from pydantic import BaseModel
from datetime import time
from .Day import Day

class Availability(BaseModel):
    """
    Represents a professor's availability.

    Attributes:
        availability_id (int): Unique identifier for the availability entry.
        professor_id (int): ID of the professor.
        day (str): Day of the week.
        start_time (time): Start of availability.
        end_time (time): End of availability.
    """
    availability_id: int
    professor_id: int
    day: Day
    start_time: time
    end_time: time