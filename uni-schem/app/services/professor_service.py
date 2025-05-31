from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate
from app.repositories import professor_repository


def register_professor(db: Session, data: ProfessorCreate) -> Professor:
    """
    Registers a new professor in the system.

    This function checks for the uniqueness of email, phone number, and DNI 
    before creating a new professor. It ensures the database transaction is 
    safely rolled back if an error occurs.

    Args:
        db (Session): The database session.
        data (ProfessorCreate): The data used to create the professor.

    Returns:
        Professor: The newly created professor object.

    Raises:
        HTTPException: If a professor with the same email, phone, or DNI already exists,
                       or if a database error occurs.
    """
    existing_professor_email = db.query(Professor).filter(Professor.email == data.email).first()
    if existing_professor_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A professor with this email already exists."
        )

    if data.phone:
        existing_professor_phone = db.query(Professor).filter(Professor.phone == data.phone).first()
        if existing_professor_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A professor with this phone number already exists."
            )

    if data.dni:
        existing_professor_dni = db.query(Professor).filter(Professor.dni == data.dni).first()
        if existing_professor_dni:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A professor with this DNI already exists."
            )

    new_professor = Professor(
        name=data.name,
        email=data.email,
        phone=data.phone,
        dni=data.dni
    )

    try:
        db.add(new_professor)
        db.commit()
        db.refresh(new_professor)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the professor: {str(e)}"
        )

    return new_professor


def get_professor(db: Session, professor_id: int) -> Optional[Professor]:
    """
    Retrieves a professor by their unique ID.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): The unique identifier of the professor.

    Returns:
        Optional[Professor]: The professor if found, else None.
    """
    return professor_repository.get_professor_by_id(db, professor_id)


def list_professors(db: Session) -> List[Professor]:
    """
    Retrieves all professors registered in the system.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Professor]: A list of all professor records.
    """
    return professor_repository.get_all_professors(db)


def get_professor_by_dni(db: Session, dni: str) -> Optional[Professor]:
    """
    Retrieves a professor by their DNI.

    Args:
        db (Session): SQLAlchemy session.
        dni (str): The DNI of the professor.

    Returns:
        Optional[Professor]: The professor if found, otherwise None.
    """
    return db.query(Professor).filter(Professor.dni == dni).first()


def modify_professor(
    db: Session, professor_id: int, updates: ProfessorUpdate
) -> Optional[Professor]:
    """
    Updates an existing professor's information, validating email and phone uniqueness.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): ID of the professor to update.
        updates (ProfessorUpdate): Fields to update (e.g., name, email, phone).

    Returns:
        Optional[Professor]: The updated professor if found, else None.
    """
    if updates.dni is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The DNI field cannot be updated."
        )
    
    if updates.email:
        existing_professor_email = db.query(Professor).filter(
            Professor.email == updates.email).first()
        if existing_professor_email and existing_professor_email.professor_id != professor_id:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A professor with this email already exists."
        )

    if updates.phone:
        existing_professor_phone = db.query(Professor).filter(
            Professor.phone == updates.phone).first()
        if existing_professor_phone and existing_professor_phone.professor_id != professor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A professor with this phone number already exists."
            )

    return professor_repository.update_professor(
        db, professor_id, updates.dict(exclude_unset=True)
    )


def remove_professor(db: Session, professor_id: int) -> bool:
    """
    Deletes a professor from the system by ID.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): The ID of the professor to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    return professor_repository.delete_professor(db, professor_id)
