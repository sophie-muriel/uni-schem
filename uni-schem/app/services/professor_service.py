from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate
from app.repositories import professor_repository


def register_professor(db: Session, professor_data: ProfessorCreate) -> Professor:
    """
    Registers a new professor after checking for duplicates.

    Args:
        db (Session): SQLAlchemy session.
        professor_data (ProfessorCreate): Input data for new professor.

    Returns:
        Professor: The created professor.

    Raises:
        ValueError: If a professor with the same ID already exists.
    """
    existing = professor_repository.get_professor_by_id(db, professor_data.professor_id)
    if existing:
        raise ValueError("Professor with this ID already exists.")

    new_professor = Professor(**professor_data.dict())
    return professor_repository.create_professor(db, new_professor)


def get_professor(db: Session, professor_id: int) -> Optional[Professor]:
    """
    Retrieves a professor by ID.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): The professor's unique identifier.

    Returns:
        Optional[Professor]: The professor if found.
    """
    return professor_repository.get_professor_by_id(db, professor_id)


def list_professors(db: Session) -> List[Professor]:
    """
    Returns a list of all professors.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Professor]: All professors in the system.
    """
    return professor_repository.get_all_professors(db)


def modify_professor(
    db: Session, professor_id: int, updates: ProfessorUpdate
) -> Optional[Professor]:
    """
    Updates a professor's information.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): ID of the professor to update.
        updates (ProfessorUpdate): Data to apply.

    Returns:
        Optional[Professor]: Updated professor if found, else None.
    """
    return professor_repository.update_professor(
        db, professor_id, updates.dict(exclude_unset=True)
    )


def remove_professor(db: Session, professor_id: int) -> bool:
    """
    Deletes a professor from the system.

    Args:
        db (Session): SQLAlchemy session.
        professor_id (int): ID of the professor to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    return professor_repository.delete_professor(db, professor_id)
