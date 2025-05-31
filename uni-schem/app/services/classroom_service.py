from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate
from app.repositories import classroom_repository
from fastapi import HTTPException, status


def register_classroom(db: Session, data: ClassroomCreate) -> Classroom:
    """
    Registers a new classroom after validating the name is unique and capacity is valid.

    Args:
        db (Session): SQLAlchemy session.
        data (ClassroomCreate): Classroom data.

    Returns:
        Classroom: The created classroom.
    """
    existing_classroom_by_name = db.query(Classroom).filter(Classroom.name == data.name).first()
    if existing_classroom_by_name:
        raise HTTPException(
            status_code=400, detail="A classroom with this name already exists."
        )

    if data.capacity < 5 or data.capacity > 40:
        raise HTTPException(
            status_code=400, detail="Classroom capacity must be between 5 and 40."
        )

    new_classroom = Classroom(
        name=data.name,
        capacity=data.capacity,
        location=data.location,
    )

    try:
        return classroom_repository.create_classroom(db, new_classroom)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the classroom."
        )


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


def modify_classroom(db: Session, classroom_id: int, updates: ClassroomUpdate) -> Classroom:
    """
    Updates the details of an existing classroom, ensuring name uniqueness
    (excluding the current classroom) and valid capacity range.

    Args:
        db (Session): Database session.
        classroom_id (int): ID of the classroom to be updated.
        updates (ClassroomUpdate): The fields to update.

    Returns:
        Classroom: The updated classroom.

    Raises:
        HTTPException: If the classroom is not found (404),
        if a duplicate name exists (400),
        if capacity is invalid (400), or for unexpected errors (500).
    """
    current_classroom = classroom_repository.get_classroom_by_id(db, classroom_id)
    if not current_classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found."
        )
    
    if updates.name is not None:
        existing_duplicate_classroom = db.query(Classroom).filter(
            Classroom.name == updates.name,
            Classroom.classroom_id != classroom_id
        ).first()

        if existing_duplicate_classroom:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A classroom with the name '{updates.name}' already exists."
            )
            
    if updates.capacity is not None:
        if updates.capacity < 5 or updates.capacity > 40:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Classroom capacity must be between 5 and 40."
            )
        
    try:
        updated_classroom = classroom_repository.update_classroom(
            db, classroom_id, updates.dict(exclude_unset=True)
        )
        return updated_classroom
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during classroom modification: {e}"
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
