from datetime import time
from pydantic import BaseModel
from .day import Day

class Availability(BaseModel):
    """
    Represents a professor's availability.

    Attributes:
        availability_id (int): Unique identifier for the availability entry.
        professor_id (int): ID of the professor assigned to this availability.
        day (Day): The day of the week when the professor is available.
        start_time (time): Start time of the availability window.
        end_time (time): End time of the availability window.
    """
    availability_id: int
    professor_id: int
    day: Day
    start_time: time
    end_time: time