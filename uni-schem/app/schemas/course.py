from typing import Optional
from pydantic import BaseModel, constr


class CourseBase(BaseModel):
    """
    Shared attributes for course models.

    Attributes:
        name (str): Full name of the course (max 100 characters).
        code (str): Code used to identify the course (max 20 characters).
        semester (str): Semester when the course is offered (max 20 characters).
        professor_id (int): The ID of the professor teaching the course.
    """
    name: constr(max_length=100)
    code: constr(max_length=20)
    semester: constr(max_length=20)
    professor_id: int


class CourseCreate(CourseBase):
    """
    Schema for creating a new course. The ID is generated by the database.

    Inherits:
        name, code, semester, professor_id from CourseBase.
    """


class CourseUpdate(BaseModel):
    """
    Schema for updating a course. All fields are optional to allow partial updates.

    Attributes:
        name (Optional[str]): Full name of the course (max 100 characters).
        code (Optional[str]): Code used to identify the course (max 20 characters).
        semester (Optional[str]): Semester when the course is offered (max 20 characters).
        professor_id (Optional[int]): The ID of the professor teaching the course.
    """
    name: Optional[constr(max_length=100)] = None
    code: Optional[constr(max_length=20)] = None
    semester: Optional[constr(max_length=20)] = None
    professor_id: Optional[int] = None


class CourseOut(CourseBase):
    """
    Schema for returning course data in API responses.

    Adds:
        course_id (int): Unique identifier for the course.
    """
    course_id: int

    class Config:
        orm_mode = True
