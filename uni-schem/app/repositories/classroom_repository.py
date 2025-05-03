from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.classroom import Classroom


def create_classroom(db: Session, classroom: Classroom) -> Classroom:
    """
    Inserts a new classroom into the database.

    Args:
        db (Session): SQLAlchemy session.
        classroom (Classroom): The classroom to insert.

    Returns:
        Classroom: The newly created classroom.
    """
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom


def get_classroom_by_id(db: Session, classroom_id: int) -> Optional[Classroom]:
    """
    Retrieves a classroom by its ID.

    Args:
        db (Session): SQLAlchemy session.
        classroom_id (int): The classroom's unique identifier.

    Returns:
        Optional[Classroom]: The classroom if found, else None.
    """
    return db.query(Classroom).filter(Classroom.classroom_id == classroom_id).first()


def get_all_classrooms(db: Session) -> List[Classroom]:
    """
    Retrieves all classrooms.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Classroom]: A list of all classrooms.
    """
    return db.query(Classroom).all()


def update_classroom(
    db: Session, classroom_id: int, updates: dict
) -> Optional[Classroom]:
    """
    Updates an existing classroom.

    Args:
        db (Session): SQLAlchemy session.
        classroom_id (int): The classroom ID.
        updates (dict): Dictionary of fields to update.

    Returns:
        Optional[Classroom]: The updated classroom or None if not found.
    """
    classroom = get_classroom_by_id(db, classroom_id)
    if not classroom:
        return None

    for key, value in updates.items():
        setattr(classroom, key, value)

    db.commit()
    db.refresh(classroom)
    return classroom


def delete_classroom(db: Session, classroom_id: int) -> bool:
    """
    Deletes a classroom from the database.

    Args:
        db (Session): SQLAlchemy session.
        classroom_id (int): The ID of the classroom to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    classroom = get_classroom_by_id(db, classroom_id)
    if not classroom:
        return False

    db.delete(classroom)
    db.commit()
    return True
