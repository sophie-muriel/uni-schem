from pydantic import BaseModel, constr
from typing import Optional

NameStr = constr(max_length=50)
LocationStr = constr(max_length=100)

class Classroom(BaseModel):
    """
    Represents a physical classroom within the institution.

    Attributes:
        classroom_id (int): Unique identifier for the classroom.
        name (str): Name or number of the classroom (max 50 characters).
        capacity (int): Maximum number of students the classroom can hold.
        location (Optional[str]): Location or building info (up to 100 characters).
    """
    classroom_id: int
    name: NameStr
    capacity: int
    location: Optional[LocationStr]