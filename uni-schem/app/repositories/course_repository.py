from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.course import Course


def create_course(db: Session, course: Course) -> Course:
    """
    Adds a new course to the database.

    Args:
        db (Session): SQLAlchemy session.
        course (Course): Course instance to add.

    Returns:
        Course: The created course.
    """
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_by_id(db: Session, course_id: int) -> Optional[Course]:
    """
    Retrieves a course by its ID.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): ID of the course.

    Returns:
        Optional[Course]: The course if found, else None.
    """
    return db.query(Course).filter(Course.course_id == course_id).first()


def get_all_courses(db: Session) -> List[Course]:
    """
    Returns all courses in the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Course]: List of all courses.
    """
    return db.query(Course).all()


def update_course(db: Session, course_id: int, updates: dict) -> Optional[Course]:
    """
    Updates a course by ID.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): ID of the course.
        updates (dict): Fields to update.

    Returns:
        Optional[Course]: The updated course if found.
    """
    course = get_course_by_id(db, course_id)
    if not course:
        return None

    for key, value in updates.items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int) -> bool:
    """
    Deletes a course by ID.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): ID of the course.

    Returns:
        bool: True if deleted, False otherwise.
    """
    course = get_course_by_id(db, course_id)
    if not course:
        return False

    db.delete(course)
    db.commit()
    return True
