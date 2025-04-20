from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
import re


class ProfessorBase(BaseModel):
    """
    Shared attributes for professor models.
    """
    name: constr(max_length=100)
    email: EmailStr
    phone: Optional[constr(max_length=15)]

    @field_validator('phone')
    def validate_phone(cls, v):
        """
        Ensure phone number is in a valid format (digits, +, (), -, space).
        """
        if v and not re.match(r'^\+?[0-9\s\-\(\)]{7,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        """
        Ensure the name only contains letters, spaces, and apostrophes.
        """
        if not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError('Name must only contain letters, spaces, or apostrophes')
        return v


class ProfessorCreate(ProfessorBase):
    """
    Schema for creating a new professor.
    """
    professor_id: int


class ProfessorUpdate(BaseModel):
    """
    Schema for updating professor data. All fields optional.
    """
    name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(max_length=15)] = None

    @field_validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?[0-9\s\-\(\)]{7,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        if v and not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError('Name must only contain letters, spaces, or apostrophes')
        return v


class ProfessorOut(ProfessorBase):
    """
    Schema used for outputting professor data.
    """
    professor_id: int

    class Config:
        orm_mode = True
