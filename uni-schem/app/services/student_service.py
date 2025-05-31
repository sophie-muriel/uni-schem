from typing import List, Optional
from sqlalchemy.orm import Session 
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.repositories import student_repository
from fastapi import HTTPException, status

def register_student(db: Session, data: StudentCreate) -> Student:
    """
    Registers a new student in the system.

    Args:
        db (Session): SQLAlchemy session.
        data (StudentCreate): Input data for the new student.

    Returns:
        Student: The newly created student object.

    Raises:
        HTTPException: If a student with the same DNI or email already exists.
    """
    existing_student_by_dni = db.query(Student).filter(Student.dni == data.dni).first()
    if existing_student_by_dni:
        raise HTTPException(
            status_code=400, detail="Student with this DNI already exists."
        )

    existing_student_by_email = db.query(Student).filter(Student.email == data.email).first()
    if existing_student_by_email:
        raise HTTPException(
            status_code=400, detail="Student with this email already exists."
        )

    new_student = Student(
        name=data.name,
        email=data.email,
        phone=data.phone,
        dni=data.dni,
    )
    return student_repository.create_student(db, new_student)

def get_student(db: Session, student_id: int) -> Optional[Student]:
    """
    Retrieves a student by their unique ID.

    Args:
        db (Session): SQLAlchemy session.
        student_id (int): The student's ID.

    Returns:
        Optional[Student]: The student object if found, otherwise None.
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
    Retrieves all students stored in the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Student]: A list of all student records.
    """
    return student_repository.get_all_students(db)


def modify_student(
    db: Session, student_id: int, updates: StudentUpdate
) -> Student:
    """
    Updates a student's data, validating email and phone uniqueness,
    and preventing DNI modification.

    Args:
        db (Session): SQLAlchemy session.
        student_id (int): ID of the student to update.
        updates (StudentUpdate): Fields to update.

    Returns:
        Optional[Student]: The updated student object, if update was successful.

    Raises:
        HTTPException: If updated email or phone already exists, or DNI modification is attempted.
    """
    current_student = student_repository.get_student_by_id(db, student_id)

    if not current_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )
    
    if updates.dni:
        if updates.dni != current_student.dni:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Modification of DNI to a different value is not allowed."
            )

    if updates.email:
        existing_email = db.query(Student).filter(
            Student.email == updates.email).first()
        if existing_email and existing_email.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A student with this email already exists."
            )

    if updates.phone:
        existing_phone = db.query(Student).filter(
            Student.phone == updates.phone).first()
        if existing_phone and existing_phone.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A student with this phone number already exists."
            )

    try:
        updated_student = student_repository.update_student(
            db, student_id, updates.dict(exclude_unset=True)
        )
        return updated_student
    except HTTPException as e: 
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )



def remove_student(db: Session, student_id: int) -> bool:
    """
    Deletes a student record from the database by ID.

    Args:
        db (Session): SQLAlchemy session.
        student_id (int): ID of the student to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    return student_repository.delete_student(db, student_id)
