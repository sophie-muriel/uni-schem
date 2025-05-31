from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator
import re


class StudentBase(BaseModel):
    """
    Shared attributes for student models.

    Attributes:
        name (str): Full name of the student (max 100 characters).
        email (EmailStr): Valid email address of the student.
        phone (Optional[str]): Contact phone number (max 10 characters).
        dni (str): Unique identifier (DNI or equivalent), length between 6 and 10.
    """
    name: constr(max_length=100)
    email: EmailStr
    phone: Optional[constr(max_length=10)] = None
    dni: constr(min_length=6, max_length=10)

    @validator('phone')
    def validate_phone(cls, v):
        """
        Validates that the phone number contains only digits and is exactly 10 digits long.

        Raises:
            ValueError: If phone is not numeric or does not have exactly 10 digits.
        """
        if v:
            if not v.isdigit():
                raise ValueError('Phone number must contain only digits')
            if len(v) != 10:
                raise ValueError('Phone number must be exactly 10 digits')
        return v

    @validator('dni')
    def validate_dni(cls, v):
        """
        Validates that the DNI contains only digits.

        Raises:
            ValueError: If DNI contains non-digit characters.
        """
        if not v.isdigit():
            raise ValueError('DNI must contain only digits')
        return v

    @validator('name')
    def validate_name(cls, v):
        """
        Validates that the name contains only letters and spaces (no accents or special characters).

        Raises:
            ValueError: If name contains invalid characters.
        """
        if not re.match("^[a-zA-Z ]*$", v):
            raise ValueError('Name must contain only letters and spaces, no accents')
        return v


class StudentCreate(StudentBase):
    """
    Schema for creating a new student.
    Inherits: name, email, phone, dni from StudentBase.
    """
    pass


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
    phone: Optional[constr(max_length=10)] = None
    dni: Optional[constr(min_length=6, max_length=10)] = None


class StudentOut(StudentBase):
    """
    Schema used for returning student data in API responses.

    Adds:
        student_id (int): Unique identifier for the student.
    """
    student_id: int

    class Config:
        orm_mode = True
