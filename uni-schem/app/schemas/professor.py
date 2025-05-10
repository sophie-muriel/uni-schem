from typing import Optional
import re
from pydantic import BaseModel, EmailStr, constr, field_validator


class ProfessorBase(BaseModel):
    """
    Shared attributes for professor models.

    Attributes:
        name (str): Full name of the professor (max 100 characters).
        email (EmailStr): Valid email address of the professor.
        phone (Optional[str]): Contact phone number (up to 15 characters).
    """
    name: constr(max_length=100)
    email: EmailStr
    phone: Optional[constr(max_length=15)] = None

    @field_validator("phone")
    def validate_phone(cls, v):
        """
        Ensure phone number is in a valid format (digits, +, (), -, space).
        """
        if v and not re.match(r"^\+?[0-9\s\-\(\)]{7,15}$", v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        """
        Ensure the name only contains letters, spaces, and apostrophes.
        """
        if not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError(
                "Name must only contain letters, spaces, or apostrophes")
        return v


class ProfessorCreate(ProfessorBase):
    """
    Schema for creating a new professor.

    Inherits:
        name, email, phone from ProfessorBase.
    """
    pass


class ProfessorUpdate(BaseModel):
    """
    Schema for updating professor data. All fields optional.

    Attributes:
        name (Optional[str]): Full name of the professor.
        email (Optional[EmailStr]): Email address of the professor.
        phone (Optional[str]): Contact phone number.
    """
    name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(max_length=15)] = None

    @field_validator("phone")
    def validate_phone(cls, v):
        if v and not re.match(r"^\+?[0-9\s\-\(\)]{7,15}$", v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        if v and not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError(
                "Name must only contain letters, spaces, or apostrophes")
        return v


class ProfessorOut(ProfessorBase):
    """
    Schema used for outputting professor data in API responses.

    Adds:
        professor_id (int): Unique identifier for the professor.
    """
    professor_id: int

    class Config:
        orm_mode = True
