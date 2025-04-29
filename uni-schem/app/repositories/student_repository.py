from sqlalchemy.orm import Session
from app.models.student import Student
from typing import List, Optional


def create_student(db: Session, student: Student) -> Student:
    """
    Adds a new student to the database.

    Args:
        db (Session): SQLAlchemy session object.
        student (Student): Student instance to be added.

    Returns:
        Student: The newly added student.
    """
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
        Optional[Student]: The student if found, or None.
    """
    return db.query(Student).filter(Student.student_id == student_id).first()


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
        updated_data (dict): Dictionary with updated fields.

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
