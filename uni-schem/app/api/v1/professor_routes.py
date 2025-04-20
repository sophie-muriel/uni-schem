from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorOut
from app.services import professor_service
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    """
    Provides a SQLAlchemy database session to endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProfessorOut)
def create_professor_route(professor: ProfessorCreate, db: Session = Depends(get_db)):
    """
    Create a new professor.
    """
    try:
        return professor_service.register_professor(db, professor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProfessorOut])
def list_professors_route(db: Session = Depends(get_db)):
    """
    Retrieve all professors.
    """
    return professor_service.list_professors(db)


@router.get("/{professor_id}", response_model=ProfessorOut)
def get_professor_route(professor_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a professor by their ID.
    """
    professor = professor_service.get_professor(db, professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@router.put("/{professor_id}", response_model=ProfessorOut)
def update_professor_route(professor_id: int, updates: ProfessorUpdate, db: Session = Depends(get_db)):
    """
    Update a professor's information.
    """
    updated = professor_service.modify_professor(db, professor_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Professor not found")
    return updated


@router.delete("/{professor_id}")
def delete_professor_route(professor_id: int, db: Session = Depends(get_db)):
    """
    Delete a professor by ID.
    """
    if not professor_service.remove_professor(db, professor_id):
        raise HTTPException(status_code=404, detail="Professor not found")
    return {"message": "Professor deleted successfully"}
