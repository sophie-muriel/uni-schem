from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.professor import Professor
from fastapi import HTTPException, status

def create_professor(db: Session, professor: Professor) -> Professor:
    """
    Creates a new professor in the database, ensuring that the email and phone number are unique.

    Args:
        db (Session): SQLAlchemy session object.
        professor (Professor): The professor instance to be added.

    Returns:
        Professor: The newly created professor.

    Raises:
        HTTPException: If the email or phone already exists in the database.
    """
    existing_email = db.query(Professor).filter(Professor.email == professor.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A professor with this email already exists."
        )

    if professor.phone:
        existing_phone = db.query(Professor).filter(Professor.phone == professor.phone).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A professor with this phone number already exists."
            )

    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor


def get_professor_by_id(db: Session, professor_id: int) -> Optional[Professor]:
    """
    Retrieves a professor by their unique ID.

    Args:
        db (Session): SQLAlchemy session object.
        professor_id (int): The ID of the professor to retrieve.

    Returns:
        Optional[Professor]: The professor if found, else None.
    """
    return db.query(Professor).filter(Professor.professor_id == professor_id).first()


def get_all_professors(db: Session) -> List[Professor]:
    """
    Retrieves all professors from the database.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[Professor]: A list of all professors.
    """
    return db.query(Professor).all()


def update_professor(
    db: Session, professor_id: int, updates: dict
) -> Optional[Professor]:
    """
    Updates an existing professor, ensuring updated email and phone number are unique.

    Args:
        db (Session): SQLAlchemy session object.
        professor_id (int): The ID of the professor to update.
        updates (dict): Dictionary containing the fields to update.

    Returns:
        Optional[Professor]: The updated professor, or None if not found.

    Raises:
        HTTPException: If the updated email or phone already exists for another professor.
    """
    professor = get_professor_by_id(db, professor_id)
    if not professor:
        return None

    if 'email' in updates:
        existing_email = db.query(Professor).filter(Professor.email == updates['email']).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A professor with this email already exists."
            )

    if 'phone' in updates:
        existing_phone = db.query(Professor).filter(Professor.phone == updates['phone']).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A professor with this phone number already exists."
            )

    for key, value in updates.items():
        setattr(professor, key, value)

    db.commit()
    db.refresh(professor)
    return professor


def delete_professor(db: Session, professor_id: int) -> bool:
    """
    Deletes a professor by their ID.

    Args:
        db (Session): SQLAlchemy session object.
        professor_id (int): The ID of the professor to delete.

    Returns:
        bool: True if the professor was deleted, False if not found.
    """
    professor = get_professor_by_id(db, professor_id)
    if not professor:
        return False

    db.delete(professor)
    db.commit()
    return True
