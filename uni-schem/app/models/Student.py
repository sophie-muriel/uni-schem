from pydantic import BaseModel, EmailStr, constr
from typing import Optional

NameStr = constr(max_length=100)
PhoneStr = constr(max_length=15)

class Student(BaseModel):
    """
    Represents a student in the academic system.

    Attributes:
        student_id (int): Unique identifier for the student.
        name (str): Full name of the student.
        email (EmailStr): Valid email address of the student.
        phone (Optional[str]): Contact phone number (up to 15 characters).
    """
    student_id: int
    name: NameStr
    email: EmailStr
    phone: Optional[PhoneStr]