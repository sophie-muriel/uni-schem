from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Classroom(Base):
    """
    Represents a physical classroom within the institution.

    Attributes:
        classroom_id (int): Unique identifier for the classroom.
        name (str): Name or number of the classroom (max 50 characters).
        capacity (int): Maximum number of students the classroom can hold.
        location (Optional[str]): Location or building info (up to 100 characters).

    Relationships:
        schedules (List[Schedule]): List of schedule entries assigned to this classroom.
    """
    __tablename__ = "classroom"

    classroom_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String(100), nullable=True)

    # Relationship back to Schedule
    schedules = relationship("Schedule", back_populates="classroom")
