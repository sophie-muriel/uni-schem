from pydantic import BaseModel
from typing import Optional


class StudentCourseBase(BaseModel):
    """
    Shared attributes for student-course relationships.

    Attributes:
        student_id (int): ID of the student in the relationship.
        course_id (int): ID of the course in the relationship.
    """
    student_id: int
    course_id: int


class StudentCourseCreate(StudentCourseBase):
    """
    Schema for creating a new enrollment.

    Inherits:
        student_id, course_id from StudentCourseBase.
    """
    pass


class StudentCourseUpdate(BaseModel):
    """
    Schema for updating a student-course relationship. All fields optional.

    Attributes:
        student_id (Optional[int]): Updated student ID.
        course_id (Optional[int]): Updated course ID.
    """
    student_id: Optional[int] = None
    course_id: Optional[int] = None


class StudentCourseOut(StudentCourseBase):
    """
    Schema for returning student-course relationship data.

    Adds:
        student_course_id (int): Unique identifier for the enrollment.
    """
    student_course_id: int

    class Config:
        orm_mode = True
