from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
import re

class Professor(BaseModel):
    """
    Represents a professor in the academic system.

    Attributes:
        professor_id (int): Unique identifier for the professor.
        name (str): Full name of the professor.
        email (EmailStr): Valid email address of the professor.
        phone (str): Contact phone number, up to 15 characters.
    """
    professor_id: int
    name: constr(max_length=100)
    email: EmailStr
    phone: constr(max_length=15)

    @field_validator('phone')
    def validate_phone(cls, v):
        """
        Custom validator to ensure the phone number matches a specific format;
        it ensures the phone contains only digits, spaces, dashes, and parentheses.
        """
        if v and not re.match(r'^\+?[0-9\s\-\(\)]{7,15}$', v):
            raise ValueError('Invalid phone number format')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        """
        Custom validator to ensure the name contains only letters, spaces, and apostrophes.
        """
        if not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError('Name must only contain letters, spaces, or apostrophes')
        return v