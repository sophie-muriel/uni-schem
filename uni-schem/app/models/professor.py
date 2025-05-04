from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Professor(Base):
    """
    Represents a professor in the academic system.

    Attributes:
        professor_id (int): Unique identifier for the professor.
        name (str): Full name of the professor.
        email (str): Valid email address of the professor.
        phone (str): Contact phone number, up to 15 characters.

    Relations:
        courses (List[Course]): Courses taught by the professor.
        availabilities (List[Availability]): Availability slots for the professor.
    """
    __tablename__ = "professor"

    professor_id   = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), nullable=False)
    email          = Column(String(320), unique=True, nullable=False)
    phone          = Column(String(15), nullable=True)

    # Relationship back to Course and Availability
    courses        = relationship("Course",       back_populates="professor")
    availabilities = relationship("Availability", back_populates="professor")
