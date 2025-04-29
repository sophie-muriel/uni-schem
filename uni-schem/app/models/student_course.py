from pydantic import BaseModel


class StudentCourse(BaseModel):
    """
    Represents the relationship between a student and a course (enrollment).

    Attributes:
        student_course_id (int): Unique ID for the enrollment.
        student_id (int): ID of the enrolled student.
        course_id (int): ID of the enrolled course.
    """

    student_course_id: int
    student_id: int
    course_id: int
