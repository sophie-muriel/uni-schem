from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class StudentBase(BaseModel):
    """
    Shared attributes for student models.

    Attributes:
        name (str): Full name of the student (max 100 characters).
        email (EmailStr): Valid email address of the student.
        phone (Optional[str]): Contact phone number (up to 15 characters).
        dni (str): Unique identifier (DNI or equivalent).
    """
    name: constr(max_length=100)
    email: EmailStr
    phone: Optional[constr(max_length=15)] = None
    dni: constr(max_length=20)


class StudentCreate(StudentBase):
    """
    Schema for creating a new student.
    Inherits: name, email, phone, dni from StudentBase.
    """


class StudentUpdate(BaseModel):
    """
    Schema for updating student data. All fields optional.

    Attributes:
        name (Optional[str]): Updated full name of the student.
        email (Optional[EmailStr]): Updated email address.
        phone (Optional[str]): Updated contact phone number.
        dni (Optional[str]): Updated DNI.
    """
    name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(max_length=15)] = None
    dni: Optional[constr(max_length=20)] = None


class StudentOut(StudentBase):
    """
    Schema used for returning student data in API responses.

    Adds:
        student_id (int): Unique identifier for the student.
    """
    student_id: int

    class Config:
        orm_mode = True
