from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories import course_repository


def register_course(db: Session, course_data: CourseCreate) -> Course:
    """
    Registers a new course after validating it doesn't already exist.

    Args:
        db (Session): SQLAlchemy session.
        course_data (CourseCreate): Incoming course data.

    Returns:
        Course: The newly created course.

    Raises:
        ValueError: If a course with the same ID already exists.
    """
    existing = course_repository.get_course_by_id(db, course_data.course_id)
    if existing:
        raise ValueError("Course with this ID already exists.")

    new_course = Course(**course_data.dict())
    return course_repository.create_course(db, new_course)


def get_course(db: Session, course_id: int) -> Optional[Course]:
    """
    Retrieves a course by ID.
    """
    return course_repository.get_course_by_id(db, course_id)


def list_courses(db: Session) -> List[Course]:
    """
    Returns a list of all courses.
    """
    return course_repository.get_all_courses(db)


def modify_course(db: Session, course_id: int, updates: CourseUpdate) -> Optional[Course]:
    """
    Updates a course with new data.
    """
    return course_repository.update_course(db, course_id, updates.dict(exclude_unset=True))


def remove_course(db: Session, course_id: int) -> bool:
    """
    Deletes a course by ID.
    """
    return course_repository.delete_course(db, course_id)