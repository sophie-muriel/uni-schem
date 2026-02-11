from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Student(Base):
    """
    Represents a student in the academic system.

    Attributes:
        student_id (int): Unique identifier for the student.
        name (str): Full name of the student.
        email (str): Valid email address of the student.
        phone (str): Contact phone number (up to 15 characters).
        dni (str): The student's DNI (identity document) or ID number.

    Relationships:
        enrollments (List[StudentCourse]): Courses the student is enrolled in.
    """
    __tablename__ = "student"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    phone = Column(String(15), nullable=True)
    dni = Column(String(20), unique=True, nullable=False)

    enrollments = relationship(
        "StudentCourse", back_populates="student", cascade="all, delete-orphan")
