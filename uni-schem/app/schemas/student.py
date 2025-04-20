from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class StudentBase(BaseModel):
    """
    Shared attributes for Student.
    """
    name: constr(max_length=100)
    email: EmailStr
    phone: Optional[constr(max_length=15)] = None


class StudentCreate(StudentBase):
    """
    Schema used to create a new student.
    """
    student_id: int


class StudentUpdate(BaseModel):
    """
    Schema used to update student data. All fields are optional.
    """
    name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(max_length=15)] = None


class StudentOut(StudentBase):
    """
    Schema used to return student data in API responses.
    """
    student_id: int

    class Config:
        orm_mode = True  # Needed for SQLAlchemy model conversion
