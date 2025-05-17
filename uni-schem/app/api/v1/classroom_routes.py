from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate, ClassroomOut
from app.services import classroom_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=ClassroomOut)
def create_classroom_route(data: ClassroomCreate, db: Session = Depends(get_db)):
    """
    Creates a new classroom entry.

    Args:
        data (ClassroomCreate): The classroom information to be registered.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ClassroomOut: The newly created classroom record.

    Raises:
        HTTPException: If a ValueError occurs during registration, returns a 400 Bad Request
        with the corresponding error message.
    """
    try:
        return classroom_service.register_classroom(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[ClassroomOut])
def list_classrooms_route(db: Session = Depends(get_db)):
    """
    Retrieves all classroom entries from the database.

    Args:
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[ClassroomOut]: A list of all registered classrooms.
    """
    return classroom_service.list_classrooms(db)


@router.get("/{classroom_id}", response_model=ClassroomOut)
def get_classroom_route(classroom_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a classroom entry by its unique ID.

    Args:
        classroom_id (int): The unique identifier of the classroom.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ClassroomOut: The requested classroom record.

    Raises:
        HTTPException: If the classroom is not found, returns a 404 Not Found error.
    """
    classroom = classroom_service.get_classroom(db, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return classroom


@router.put("/{classroom_id}", response_model=ClassroomOut)
def update_classroom_route(
    classroom_id: int, updates: ClassroomUpdate, db: Session = Depends(get_db)
):
    """
    Updates an existing classroom entry by its ID.

    Args:
        classroom_id (int): The unique identifier of the classroom to update.
        updates (ClassroomUpdate): The data containing the fields to be updated.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ClassroomOut: The updated classroom record.

    Raises:
        HTTPException: If the classroom is not found, returns a 404 Not Found error.
    """
    updated = classroom_service.modify_classroom(db, classroom_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return updated


@router.delete("/{classroom_id}")
def delete_classroom_route(classroom_id: int, db: Session = Depends(get_db)):
    """
    Deletes a classroom entry by its ID.

    Args:
        classroom_id (int): The unique identifier of the classroom to delete.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        dict: A confirmation message indicating successful deletion.

    Raises:
        HTTPException: If the classroom is not found, returns a 404 Not Found error.
    """
    if not classroom_service.remove_classroom(db, classroom_id):
        raise HTTPException(status_code=404, detail="Classroom not found")
    return {"message": "Classroom deleted successfully"}
