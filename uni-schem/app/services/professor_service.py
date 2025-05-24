from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate
from app.repositories import professor_repository


def register_professor(db: Session, data: ProfessorCreate) -> Professor:
    """
    Registers a new professor.

    Args:
        db (Session): SQLAlchemy session.
        data (ProfessorCreate): Input data for the professor.

    Returns:
        Professor: The newly created professor.
    """
    new_professor = Professor(
        name=data.name,
        email=data.email,
        phone=data.phone,
    )
    return professor_repository.create_professor(db, new_professor)


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


def modify_professor(
    db: Session, professor_id: int, updates: ProfessorUpdate
) -> Optional[Professor]:
    """
    Updates an existing professor's information.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): ID of the professor to update.
        updates (ProfessorUpdate): Fields to update (e.g., name, email, phone).

    Returns:
        Optional[Professor]: The updated professor if found, else None.
    """
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
