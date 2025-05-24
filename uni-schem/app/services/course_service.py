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
    Retrieves a course by ID.
    """
    return course_repository.get_course_by_id(db, course_id)


def get_course_by_name(db: Session, name: str) -> Optional[Course]:
    """
    Retrieves a course by its name.
    """
    return course_repository.get_course_by_name(db, name)


def list_courses(db: Session) -> List[Course]:
    """
    Returns a list of all courses.
    """
    return course_repository.get_all_courses(db)


def get_courses_by_professor_id(db: Session, professor_id: int) -> List[Course]:
    """
    Retrieves courses by professor ID.
    """
    return course_repository.get_courses_by_professor_id(db, professor_id)


def modify_course(db: Session, course_id: int, updates: CourseUpdate) -> Optional[Course]:
    """
    Updates a course with new data.
    """
    return course_repository.update_course(
        db, course_id, updates.dict(exclude_unset=True)
    )


def remove_course(db: Session, course_id: int) -> bool:
    """
    Deletes a course by ID.
    """
    return course_repository.delete_course(db, course_id)
