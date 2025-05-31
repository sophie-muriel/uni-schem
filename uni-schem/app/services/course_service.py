from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories import course_repository
from fastapi import HTTPException, status
from app.repositories import professor_repository


def register_course(db: Session, data: CourseCreate) -> Course:
    """
    Registers a new course, ensuring the course code is unique.
    Course names can be repeated.

    Args:
        db (Session): SQLAlchemy session.
        data (CourseCreate): Incoming course data.

    Returns:
        Course: The newly created course.

    Raises:
        HTTPException: If a course with the same code already exists (400),
        or for unexpected internal errors (500).
    """
    if data.code:
        existing_course_by_code = db.query(Course).filter(
            Course.code == data.code
        ).first()
        if existing_course_by_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A course with code '{data.code}' already exists."
            )
    
    new_course = Course(
        name=data.name,
        code=data.code,
        semester=data.semester,
        professor_id=data.professor_id,
    )

    try:
        return course_repository.create_course(db, new_course)
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the course: {e}"
        )


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


def modify_course(db: Session, course_id: int, updates: CourseUpdate) -> Course: # Cambiamos a 'Course' (no Optional)
    """
    Updates a course with the provided fields, ensuring uniqueness of the course code
    if updated, and validating the existence of the associated professor.

    Args:
        db (Session): SQLAlchemy session.
        course_id (int): The ID of the course to update.
        updates (CourseUpdate): The fields to update.

    Returns:
        Course: The updated course.

    Raises:
        HTTPException: If the course to update is not found (404),
        if the new course code already exists for another course (400),
        if the associated professor is not found (404),
        or for unexpected internal errors (500).
    """
    current_course = course_repository.get_course_by_id(db, course_id)
    if not current_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    if updates.code is not None:
        existing_course_by_code = db.query(Course).filter(
            Course.code == updates.code
        ).first()

        if existing_course_by_code and existing_course_by_code.course_id != course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A course with code '{updates.code}' already exists."
            )

    if updates.professor_id is not None:
        professor = professor_repository.get_professor_by_id(db, updates.professor_id)
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor not found."
            )

    try:
        updated_course = course_repository.update_course(
            db, course_id, updates.dict(exclude_unset=True)
        )
        return updated_course
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during course modification: {e}"
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
