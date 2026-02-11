from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.course import Course
from app.models.professor import Professor
from fastapi import HTTPException, status
from app.models.schedule import Schedule


def create_course(db: Session, course: Course) -> Course:
    """
    Adds a new course to the database.
    Assumes business validations (like unique code and professor existence)
    have been performed at the service layer.

    Args:
        db (Session): SQLAlchemy session.
        course (Course): Course instance to add.

    Returns:
        Course: The created course with its generated ID.

    Raises:
        HTTPException: For database integrity errors (e.g., unique constraint violation for code)
        or other unexpected internal errors (500).
    """
    try:
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad requestt"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected database error occurred while creating the course: {e}"
        )


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


def get_course_by_name(db: Session, name: str) -> Optional[Course]:
    """
    Retrieves a course by its name.

    Args:
        db (Session): SQLAlchemy session.
        name (str): Name of the course.

    Returns:
        Optional[Course]: The course if found, else None.
    """
    return db.query(Course).filter(Course.name == name).first()


def get_courses_by_professor_id(db: Session, professor_id: int) -> List[Course]:
    """
    Retrieves courses by professor ID.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): Professor's unique ID.

    Returns:
        List[Course]: List of courses assigned to the professor.
    """
    return db.query(Course).filter(Course.professor_id == professor_id).all()


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    for key, value in updates.items():
        setattr(course, key, value)

    try:
        db.commit()
        db.refresh(course)
        return course
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected database error occurred while creating the course: {e}"
        )


def delete_course(db: Session, course_id: int) -> bool:
    """
    Deletes a course and updates all related schedule entries by setting course_id to NULL.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): ID of the course to delete.

    Returns:
        bool: True if the course was successfully deleted, False otherwise.
    """
    course = get_course_by_id(db, course_id)
    if not course:
        return False

    db.query(Schedule).filter(Schedule.course_id == course_id).update(
        {"course_id": None}, synchronize_session=False)
    course = db.query(Course).filter(Course.course_id == course_id).first()

    if not course:
        return False

    db.delete(course)
    db.commit()
    return True
