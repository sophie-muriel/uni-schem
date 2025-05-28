from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorOut
from app.services import professor_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=ProfessorOut)
def create_professor_route(professor: ProfessorCreate, db: Session = Depends(get_db)):
    """
    Creates a new professor entry.

    Args:
        professor (ProfessorCreate): The professor data to be registered.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ProfessorOut: The newly created professor record.

    Raises:
        HTTPException: If a ValueError occurs during registration, returns a 400 Bad Request
        with the error message.
    """
    try:
        return professor_service.register_professor(db, professor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[ProfessorOut])
def list_professors_route(db: Session = Depends(get_db)):
    """
    Retrieves all professors.

    Args:
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[ProfessorOut]: A list of all registered professors.
    """
    return professor_service.list_professors(db)


@router.get("/{professor_id}", response_model=ProfessorOut)
def get_professor_route(professor_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a professor entry by their unique ID.

    Args:
        professor_id (int): The unique identifier of the professor.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ProfessorOut: The requested professor record.

    Raises:
        HTTPException: If the professor is not found, returns a 404 Not Found error.
    """
    professor = professor_service.get_professor(db, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@router.get("/dni/{dni}", response_model=ProfessorOut)
def get_professor_by_dni_route(dni: str, db: Session = Depends(get_db)):
    """
    Retrieves a professor by their DNI.

    Args:
        dni (str): The DNI of the professor.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ProfessorOut: The requested professor record.

    Raises:
        HTTPException: If the professor is not found, returns a 404 Not Found error.
    """
    professor = professor_service.get_professor_by_dni(db, dni)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@router.put("/{professor_id}", response_model=ProfessorOut)
def update_professor_route(
    professor_id: int, updates: ProfessorUpdate, db: Session = Depends(get_db)
):
    """
    Updates an existing professor's information by their ID.

    Args:
        professor_id (int): The unique identifier of the professor to update.
        updates (ProfessorUpdate): The data containing updated fields.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        ProfessorOut: The updated professor record.

    Raises:
        HTTPException: If the professor is not found, returns a 404 Not Found error.
    """
    updated = professor_service.modify_professor(db, professor_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Professor not found")
    return updated


@router.delete("/{professor_id}")
def delete_professor_route(professor_id: int, db: Session = Depends(get_db)):
    """
    Deletes a professor entry by their ID.

    Args:
        professor_id (int): The unique identifier of the professor to delete.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        dict: A confirmation message indicating successful deletion.

    Raises:
        HTTPException: If the professor is not found, returns a 404 Not Found error.
    """
    if not professor_service.remove_professor(db, professor_id):
        raise HTTPException(status_code=404, detail="Professor not found")
    return {"message": "Professor deleted successfully"}
