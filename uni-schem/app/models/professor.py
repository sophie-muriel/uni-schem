from pydantic import BaseModel, EmailStr, constr
from typing import Optional

NameStr = constr(max_length=100)
PhoneStr = constr(max_length=15)

class Professor(BaseModel):
    """
    Represents a professor in the academic system.

    Attributes:
        professor_id (int): Unique identifier for the professor.
        name (str): Full name of the professor.
        email (EmailStr): Valid email address of the professor.
        phone (Optional[str]): Contact phone number (up to 15 characters).
    """
    professor_id: int
    name: NameStr
    email: EmailStr
    phone: Optional[PhoneStr]