from pydantic import BaseModel

class StudentCourseBase(BaseModel):
    """
    Shared attributes for student-course relationships.
    """
    student_id: int
    course_id: int


class StudentCourseCreate(StudentCourseBase):
    """
    Schema for creating a new enrollment.
    """
    student_course_id: int


class StudentCourseUpdate(BaseModel):
    """
    Schema for updating a student-course relationship. All fields optional.
    """
    student_id: int | None = None
    course_id: int | None = None


class StudentCourseOut(StudentCourseBase):
    """
    Schema for returning student-course relationship data.
    """
    student_course_id: int

    class Config:
        orm_mode = True