from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.repositories import student_repository


def register_student(db: Session, student: StudentCreate) -> Student:
    """
    Registers a new student after verifying they do not already exist.

    Args:
        db (Session): SQLAlchemy session.
        student_data (StudentCreate): Pydantic model with student input data.

    Returns:
        Student: The created student object.

    Raises:
        ValueError: If a student with the same ID already exists.
    """
    existing = student_repository.get_student_by_id(db, student.student_id)
    if existing:
        raise ValueError("Student whit this ID already exists")
    new_student = Student(**student.dict())
    return student_repository.create_student(db, new_student)


def get_student(db: Session, student_id: int) -> Optional[Student]:
    """
    Fetches a student by their ID.
    """
    return student_repository.get_student_by_id(db, student_id)


def list_students(db: Session) -> List[Student]:
    """
    Returns all students.
    """
    return student_repository.get_all_students(db)


def modify_student(
    db: Session, student_id: int, updates: StudentUpdate
) -> Optional[Student]:
    """
    Updates the student with the provided data.
    """
    return student_repository.update_student(
        db, student_id, updates.dict(exclude_unset=True)
    )


def remove_student(db: Session, student_id: int) -> bool:
    """
    Deletes a student by ID.
    """
    return student_repository.delete_student(db, student_id)
