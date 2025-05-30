from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate
from app.repositories import classroom_repository


def register_classroom(db: Session, data: ClassroomCreate) -> Classroom:
    """
    Registers a new classroom after validating the name is unique.

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
    Retrieves a classroom by its unique ID.

    Args:
        db (Session): Database session.
        classroom_id (int): The ID of the classroom.

    Returns:
        Optional[Classroom]: The classroom object if found, otherwise None.
    """
    return classroom_repository.get_classroom_by_id(db, classroom_id)


def list_classrooms(db: Session) -> List[Classroom]:
    """
    Retrieves a list of all classrooms in the system.

    Args:
        db (Session): Database session.

    Returns:
        List[Classroom]: A list of all classroom records.
    """
    return classroom_repository.get_all_classrooms(db)


def get_classrooms_by_capacity(db: Session, capacity: int) -> List[Classroom]:
    """
    Retrieves classrooms that match the given capacity.

    Args:
        db (Session): Database session.
        capacity (int): The desired classroom capacity to filter by.

    Returns:
        List[Classroom]: A list of classrooms with the specified capacity.
    """
    return classroom_repository.get_classroom_by_capacity(db, capacity)


def modify_classroom(db: Session, classroom_id: int, updates: ClassroomUpdate) -> Optional[Classroom]:
    """
    Updates the details of an existing classroom.

    Args:
        db (Session): Database session.
        classroom_id (int): ID of the classroom to be updated.
        updates (ClassroomUpdate): The fields to update.

    Returns:
        Optional[Classroom]: The updated classroom, or None if not found.
    """
    return classroom_repository.update_classroom(
        db, classroom_id, updates.dict(exclude_unset=True)
    )


def remove_classroom(db: Session, classroom_id: int) -> bool:
    """
    Deletes a classroom by its ID.

    Args:
        db (Session): Database session.
        classroom_id (int): ID of the classroom to delete.

    Returns:
        bool: True if deletion was successful, False if the classroom was not found.
    """
    return classroom_repository.delete_classroom(db, classroom_id)
