from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Course(Base):
    """
    Represents a course taught by a professor.

    Attributes:
        course_id (int): Unique identifier for the course.
        name (str): Full name of the course.
        code (str): Code used to identify the course.
        semester (str): Semester when the course is offered.
        professor_id (int): The ID of the professor assigned to the course.

    Relationships:
        professor (Professor): The professor teaching the course.
        schedules (List[Schedule]): The schedule entries for this course.
        enrollments (List[StudentCourse]): Student enrollments in this course.
    """
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    semester = Column(String(20), nullable=False)
    professor_id = Column(Integer, ForeignKey(
        "professor.professor_id"), nullable=False)

    professor = relationship("Professor", back_populates="courses")
    schedules = relationship("Schedule", back_populates="course")
    enrollments = relationship(
        "StudentCourse", back_populates="course", cascade="all, delete-orphan")
