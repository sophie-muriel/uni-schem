from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.student import Student
from fastapi import HTTPException, status


def create_student(db: Session, student: Student) -> Student:
    """
    Adds a new student to the database after validating the DNI is unique.

    Args:
        db (Session): SQLAlchemy session object.
        student (Student): The student instance to add.

    Returns:
        Student: The newly added student.

    Raises:
        HTTPException: If the DNI already exists in the database.
    """

    existing_student = db.query(Student).filter(
        Student.dni == student.dni).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this DNI already exists."
        )
    
    existing_student_by_email = db.query(Student).filter(
        Student.email == student.email).first()
    if existing_student_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this email already exists."
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
) -> Student:
    """
    Updates a student by ID, ensuring email and phone uniqueness,
    and preventing modification of DNI.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): ID of the student to update.
        updated_data (dict): Fields to be updated.

    Returns:
        Optional[Student]: The updated student or None if not found.

    Raises:
        HTTPException: If updated email or phone already exists, or DNI modification is attempted.
    """
    student = get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    if "email" in updated_data:
        existing_email = db.query(Student).filter(
            Student.email == updated_data["email"]).first()
        if existing_email and existing_email.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A student with this email already exists."
            )

    if "phone" in updated_data:
        existing_phone = db.query(Student).filter(
            Student.phone == updated_data["phone"]).first()
        if existing_phone and existing_phone.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A student with this phone number already exists."
            )

    for key, value in updated_data.items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone number already exists."
        )


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
