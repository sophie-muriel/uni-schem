from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories import course_repository


def register_course(db: Session, data: CourseCreate) -> Course:
    """
    Registers a new course.

    Args:
        db (Session): SQLAlchemy session.
        data (CourseCreate): Incoming course data.

    Returns:
        Course: The newly created course.
    """
    new_course = Course(
        name=data.name,
        code=data.code,
        semester=data.semester,
        professor_id=data.professor_id,
    )
    return course_repository.create_course(db, new_course)


def get_course(db: Session, course_id: int) -> Optional[Course]:
    """
    Retrieves a course by its unique ID.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): The unique identifier of the course.

    Returns:
        Optional[Course]: The course if found, else None.
    """
    return course_repository.get_course_by_id(db, course_id)


def get_course_by_name(db: Session, name: str) -> Optional[Course]:
    """
    Retrieves a course by its name.

    Args:
        db (Session): SQLAlchemy session.
        name (str): The name of the course.

    Returns:
        Optional[Course]: The course if found, else None.
    """
    return course_repository.get_course_by_name(db, name)


def list_courses(db: Session) -> List[Course]:
    """
    Retrieves all courses in the system.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Course]: A list of all courses.
    """
    return course_repository.get_all_courses(db)


def get_courses_by_professor_id(db: Session, professor_id: int) -> List[Course]:
    """
    Retrieves all courses assigned to a specific professor.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): The ID of the professor.

    Returns:
        List[Course]: A list of courses taught by the given professor.
    """
    return course_repository.get_courses_by_professor_id(db, professor_id)


def modify_course(db: Session, course_id: int, updates: CourseUpdate) -> Optional[Course]:
    """
    Updates a course with the provided fields.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): The ID of the course to update.
        updates (CourseUpdate): The fields to update.

    Returns:
        Optional[Course]: The updated course if found, else None.
    """
    return course_repository.update_course(
        db, course_id, updates.dict(exclude_unset=True)
    )


def remove_course(db: Session, course_id: int) -> bool:
    """
    Deletes a course by its ID.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): The ID of the course to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    return course_repository.delete_course(db, course_id)
