from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.repositories import student_repository
from fastapi import HTTPException


def register_student(db: Session, data: StudentCreate) -> Student:
    """
    Registers a new student.

    Args:
        db (Session): SQLAlchemy session.
        data (StudentCreate): Input data for the student.

    Returns:
        Student: The newly created student.
    """

    existing_student_by_dni = db.query(Student).filter(
        Student.dni == data.dni).first()
    if existing_student_by_dni:
        raise HTTPException(
            status_code=400, detail="Student with this DNI already exists.")

    new_student = Student(
        name=data.name,
        email=data.email,
        phone=data.phone,
        dni=data.dni,
    )
    return student_repository.create_student(db, new_student)


def get_student(db: Session, student_id: int) -> Optional[Student]:
    """
    Fetches a student by their ID.
    """
    return student_repository.get_student_by_id(db, student_id)


def get_student_by_dni(db: Session, dni: str) -> Optional[Student]:
    """
    Retrieves a student by their DNI.

    Args:
        db (Session): SQLAlchemy session.
        dni (str): The DNI of the student.

    Returns:
        Optional[Student]: The student record if found.
    """
    return student_repository.get_student_by_dni(db, dni)


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
