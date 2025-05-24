from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from sqlalchemy.exc import SQLAlchemyError


def create_classroom(db: Session, classroom: Classroom) -> Classroom:
    """
    Inserts a new classroom into the database with transactional control to avoid auto-increment issues.

    Args:
        db (Session): SQLAlchemy session.
        classroom (Classroom): The classroom to insert.

    Returns:
        Classroom: The newly created classroom.

    Raises:
        SQLAlchemyError: If an error occurs during insertion, raises an exception to prevent ID increment.
    """
    try:
        existing_classroom = db.query(Classroom).filter(Classroom.name == classroom.name).first()
        if existing_classroom:
            raise SQLAlchemyError("Classroom with this name already exists.")
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom
    except SQLAlchemyError as e:
        db.rollback()  
        raise e  


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


def get_classroom_by_capacity(db: Session, capacity: int) -> List[Classroom]:
    """
    Retrieves classrooms by their capacity.

    Args:
        db (Session): SQLAlchemy session.
        capacity (int): The capacity of the classroom to search for.

    Returns:
        List[Classroom]: A list of classrooms matching the capacity.
    """
    return db.query(Classroom).filter(Classroom.capacity == capacity).all()


def get_all_classrooms(db: Session) -> List[Classroom]:
    """
    Retrieves all classrooms.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Classroom]: A list of all classrooms.
    """
    return db.query(Classroom).all()


def update_classroom(db: Session, classroom_id: int, updates: dict) -> Optional[Classroom]:
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
