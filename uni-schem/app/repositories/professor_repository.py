from sqlalchemy.orm import Session
from app.models.professor import Professor
from typing import List, Optional


def create_professor(db: Session, professor: Professor) -> Professor:
    """
    Adds a new professor to the database.

    Args:
        db (Session): SQLAlchemy session object.
        professor (Professor): The professor instance to insert.

    Returns:
        Professor: The newly created professor.
    """
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


def update_professor(db: Session, professor_id: int, updates: dict) -> Optional[Professor]:
    """
    Updates an existing professor's data.

    Args:
        db (Session): SQLAlchemy session object.
        professor_id (int): The ID of the professor to update.
        updates (dict): Dictionary containing fields to update.

    Returns:
        Optional[Professor]: The updated professor, or None if not found.
    """
    professor = get_professor_by_id(db, professor_id)
    if not professor:
        return None

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