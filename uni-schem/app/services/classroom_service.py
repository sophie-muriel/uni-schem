from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate
from app.repositories import classroom_repository

def register_classroom(db: Session, data: ClassroomCreate) -> Classroom:
    """
    Registers a new classroom.

    Args:
        db (Session): SQLAlchemy session.
        data (ClassroomCreate): Classroom data.

    Returns:
        Classroom: The created classroom.
    """

    new_classroom = Classroom(
        name=data.name,
        capacity=data.capacity,
        location=data.location,
    )
    return classroom_repository.create_classroom(db, new_classroom)

def get_classroom(db: Session, classroom_id: int) -> Optional[Classroom]:
    """
    Retrieves a classroom by ID.
    """
    return classroom_repository.get_classroom_by_id(db, classroom_id)

def list_classrooms(db: Session) -> List[Classroom]:
    """
    Retrieves all classrooms.
    """
    return classroom_repository.get_all_classrooms(db)

def modify_classroom(
    db: Session, classroom_id: int, updates: ClassroomUpdate
) -> Optional[Classroom]:
    """
    Updates an existing classroom.
    """
    return classroom_repository.update_classroom(
        db, classroom_id, updates.dict(exclude_unset=True)
    )

def remove_classroom(db: Session, classroom_id: int) -> bool:
    """
    Deletes a classroom from the system.
    """
    return classroom_repository.delete_classroom(db, classroom_id)
