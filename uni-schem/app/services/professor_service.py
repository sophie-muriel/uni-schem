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
    Retrieves a professor by ID.
    """
    return professor_repository.get_professor_by_id(db, professor_id)

def list_professors(db: Session) -> List[Professor]:
    """
    Returns a list of all professors.
    """
    return professor_repository.get_all_professors(db)

def modify_professor(
    db: Session, professor_id: int, updates: ProfessorUpdate
) -> Optional[Professor]:
    """
    Updates a professor's information.
    """
    return professor_repository.update_professor(
        db, professor_id, updates.dict(exclude_unset=True)
    )

def remove_professor(db: Session, professor_id: int) -> bool:
    """
    Deletes a professor from the system.
    """
    return professor_repository.delete_professor(db, professor_id)
