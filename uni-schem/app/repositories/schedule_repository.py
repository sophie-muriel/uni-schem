from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student import Student
from fastapi import HTTPException, status


def create_student(db: Session, student: Student) -> Student:
    """
    Adds a new student to the database after validating the DNI is unique.

    Args:
        db (Session): SQLAlchemy session object.
        student (Student): Student instance to be added.

    Returns:
        Student: The newly added student.

    Raises:
        HTTPException: If a student with the same DNI already exists, raises a 400 error.
    """
    existing_student = db.query(Student).filter(
        Student.dni == student.dni).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student with this DNI already exists."
        )

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student_by_id(db: Session, student_id: int) -> Optional[Student]:
    """
    Retrieves a student by their ID.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): The ID of the student.

    Returns:
        Optional[Student]: The student if found, else None.
    """
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_by_dni(db: Session, dni: str) -> Optional[Student]:
    """
    Retrieves a student by their DNI.

    Args:
        db (Session): SQLAlchemy session object.
        dni (str): The DNI of the student.

    Returns:
        Optional[Student]: The student if found, else None.
    """
    return db.query(Student).filter(Student.dni == dni).first()


def get_all_students(db: Session) -> List[Student]:
    """
    Retrieves all students.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[Student]: List of all students in the database.
    """
    return db.query(Student).all()


def update_student(
    db: Session, student_id: int, updated_data: dict
) -> Optional[Student]:
    """
    Updates a student by ID.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): ID of the student to update.
        updated_data (dict): Fields to be updated.

    Returns:
        Optional[Student]: The updated student or None if not found.
    """
    student = get_student_by_id(db, student_id)
    if not student:
        return None

    for key, value in updated_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> bool:
    """
    Deletes a student by ID.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): ID of the student to delete.

    Returns:
        bool: True if deleted, False otherwise.
    """
    student = get_student_by_id(db, student_id)
    if not student:
        return False

    db.delete(student)
    db.commit()
    return True
