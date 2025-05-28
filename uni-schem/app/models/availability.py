from sqlalchemy import Column, Integer, ForeignKey, Time, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.day import Day


class Availability(Base):
    """
    Represents a professor's availability.

    Attributes:
        availability_id (int): Unique identifier for the availability entry.
        professor_id (int): ID of the professor assigned to this availability.
        day (Day): The day of the week when the professor is available.
        start_time (time): Start time of the availability window.
        end_time (time): End time of the availability window.
    """
    __tablename__ = "availability"

    availability_id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professor.professor_id", ondelete="SET NULL"), nullable=True)
    day = Column(SQLEnum(Day), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    professor = relationship("Professor", back_populates="availabilities")
