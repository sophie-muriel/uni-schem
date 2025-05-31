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
        dni (str): DNI (identity document) of the professor (6 to 10 digits).
    """
    name: constr(max_length=100)
    email: EmailStr
    phone: Optional[constr(max_length=15)] = None
    dni: constr(min_length=6, max_length=10)

    @field_validator("phone")
    def validate_phone(cls, v):
        """
        Ensure phone number is exactly 10 digits.
        Raises:
            ValueError: If the phone number does not have exactly 10 digits.
        """
        if v and not re.match(r"^\d{10}$", v):
            raise ValueError("Phone number must be exactly 10 digits")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        """
        Ensure the name only contains letters (without accents), spaces, and apostrophes.
        Raises:
            ValueError: If the name contains invalid characters (e.g., accented letters or special characters).
        """
        if not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError("Name must only contain letters, spaces, or apostrophes")
        return v

    @field_validator("dni")
    def validate_dni(cls, v):
        """
        Ensure the DNI consists of 6 to 10 digits.
        """
        if not re.match(r"^\d{6,10}$", v):
            raise ValueError("DNI must be between 6 and 10 digits")
        return v


class ProfessorCreate(ProfessorBase):
    """
    Schema for creating a new professor.

    Inherits:
        name, email, phone from ProfessorBase.
    """


class ProfessorUpdate(BaseModel):
    """
    Schema for updating professor data. All fields optional.

    Attributes:
        name (Optional[str]): Full name of the professor.
        email (Optional[EmailStr]): Email address of the professor.
        phone (Optional[str]): Contact phone number.
        dni (Optional[str]): DNI of the professor.
    """
    name: Optional[constr(max_length=100)] = None
    email: Optional[EmailStr] = None
    phone: Optional[constr(max_length=15)] = None
    dni: Optional[constr(min_length=6, max_length=10)] = None

    @field_validator("phone")
    def validate_phone(cls, v):
        """
        Validates the phone number format for updates.

        Args:
            v (str): The phone number value.

        Raises:
            ValueError: If the phone number does not have exactly 10 digits.

        Returns:
            str: The validated phone number.
        """
        if v and not re.match(r"^\d{10}$", v):
            raise ValueError("Phone number must be exactly 10 digits")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        """
        Validates the name format for updates.

        Args:
            v (str): The name value.

        Raises:
            ValueError: If the name contains characters outside letters, spaces, or apostrophes.

        Returns:
            str: The validated name.
        """
        if v and not re.match(r"^[A-Za-z\s']+$", v):
            raise ValueError("Name must only contain letters, spaces, or apostrophes")
        return v

    @field_validator("dni")
    def validate_dni(cls, v):
        """
        Validates the DNI format for updates.

        Args:
            v (str): The DNI value.

        Raises:
            ValueError: If the DNI is not between 6 and 10 digits.

        Returns:
            str: The validated DNI.
        """
        if v and not re.match(r"^\d{6,10}$", v):
            raise ValueError("DNI must be between 6 and 10 digits")
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
