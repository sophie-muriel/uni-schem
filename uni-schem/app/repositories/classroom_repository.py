from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from fastapi import HTTPException, status
from app.models.schedule import Schedule


def create_classroom(db: Session, classroom: Classroom) -> Classroom:
    """
    Inserts a new classroom into the database with transactional control to avoid auto-increment
    issues and validates that the classroom name is unique.

    Args:
        db (Session): SQLAlchemy session.
        classroom (Classroom): The classroom to insert.

    Returns:
        Classroom: The newly created classroom.

    Raises:
        HTTPException: If a classroom with the same name already exists, raises 400 Bad Request.
    """
    existing_classroom = db.query(Classroom).filter(
        Classroom.name == classroom.name).first()
    if existing_classroom:
        raise HTTPException(
            status_code=400,
            detail="A classroom with this name already exists."
        )

    if classroom.capacity < 5 or classroom.capacity > 40:
        raise HTTPException(
            status_code=400,
            detail="Classroom capacity must be between 5 and 40."
        )

    try:
        db.add(classroom)
        db.commit()
        db.refresh(classroom)
        return classroom
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the classroom."
        )


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
    Deletes a classroom and updates all related schedule entries by setting classroom_id to NULL.

    Args:
        db (Session): SQLAlchemy session.
        classroom_id (int): ID of the classroom to delete.

    Returns:
        bool: True if the classroom was successfully deleted, False otherwise.
    """
    db.query(Schedule).filter(Schedule.classroom_id == classroom_id).update(
        {"classroom_id": None}, synchronize_session=False)

    classroom = get_classroom_by_id(db, classroom_id)
    if not classroom:
        return False

    db.delete(classroom)
    db.commit()
    return True
