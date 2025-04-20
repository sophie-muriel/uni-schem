from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.student_course import StudentCourse
from app.schemas.student_course import StudentCourseCreate, StudentCourseUpdate
from app.repositories import student_course_repository


def register_student_course(db: Session, data: StudentCourseCreate) -> StudentCourse:
    """
    Registers a new student-course enrollment.

    Args:
        db (Session): SQLAlchemy session object.
        data (StudentCourseCreate): Data for the new enrollment.

    Returns:
        StudentCourse: The created enrollment.

    Raises:
        ValueError: If an enrollment with the same ID already exists.
    """
    existing = student_course_repository.get_student_course_by_id(db, data.student_course_id)
    if existing:
        raise ValueError("This student-course enrollment already exists.")

    new_relation = StudentCourse(**data.dict())
    return student_course_repository.create_student_course(db, new_relation)


def get_student_course(db: Session, relation_id: int) -> Optional[StudentCourse]:
    """
    Retrieves an enrollment by ID.
    """
    return student_course_repository.get_student_course_by_id(db, relation_id)


def list_student_courses(db: Session) -> List[StudentCourse]:
    """
    Retrieves all student-course enrollments.
    """
    return student_course_repository.get_all_student_courses(db)


def modify_student_course(db: Session, relation_id: int, updates: StudentCourseUpdate) -> Optional[StudentCourse]:
    """
    Updates an existing enrollment.
    """
    return student_course_repository.update_student_course(db, relation_id, updates.dict(exclude_unset=True))


def remove_student_course(db: Session, relation_id: int) -> bool:
    """
    Deletes an enrollment by ID.
    """
    return student_course_repository.delete_student_course(db, relation_id)