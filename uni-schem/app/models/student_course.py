from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class StudentCourse(Base):
    """
    Represents the relationship between a student and a course (enrollment).

    Attributes:
        student_course_id (int): Unique ID for the enrollment.
        student_id (int): ID of the enrolled student.
        course_id (int): ID of the enrolled course.

    Relationships:
        student (Student): The student enrolled in the course.
        course  (Course): The course the student is enrolled in.
    """
    __tablename__ = "student_course"

    student_course_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey(
        "student.student_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.course_id", ondelete="CASCADE"), nullable=True)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course",  back_populates="enrollments")
