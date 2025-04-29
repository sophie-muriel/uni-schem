from pydantic import BaseModel, constr
from typing import Optional


class ClassroomBase(BaseModel):
    """
    Shared attributes for classroom models.
    """

    name: constr(max_length=50)
    capacity: int
    location: Optional[constr(max_length=100)] = None


class ClassroomCreate(ClassroomBase):
    """
    Schema for creating a new classroom.
    """

    classroom_id: int


class ClassroomUpdate(BaseModel):
    """
    Schema for updating a classroom. All fields optional.
    """

    name: Optional[constr(max_length=50)] = None
    capacity: Optional[int] = None
    location: Optional[constr(max_length=100)] = None


class ClassroomOut(ClassroomBase):
    """
    Schema for returning classroom data in responses.
    """

    classroom_id: int

    class Config:
        orm_mode = True
