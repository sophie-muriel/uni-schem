from datetime import time
from sqlalchemy import Column, Integer, Time, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.day import Day


class Schedule(Base):
    """
    Represents the schedule for a course in a specific classroom.

    Attributes:
        schedule_id (int): Unique identifier for the schedule.
        course_id (int): ID of the course this schedule belongs to.
        day (Day): Day of the week.
        start_time (time): Start time of the session.
        end_time (time): End time of the session.
        classroom_id (int): ID of the classroom assigned.

    Relationships:
        course (Course): The course being scheduled.
        classroom (Classroom): The classroom assigned to this session.
    """
    __tablename__ = "schedule"

    schedule_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), nullable=False)
    day = Column(SQLEnum(Day), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    classroom_id = Column(Integer, ForeignKey(
        "classroom.classroom_id"), nullable=False)

    # Relationships back to Course and Classroom
    course = relationship("Course",     back_populates="schedules")
    classroom = relationship("Classroom",  back_populates="schedules")
