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
    Create a new classroom entry.
    """
    try:
        return classroom_service.register_classroom(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[ClassroomOut])
def list_classrooms_route(db: Session = Depends(get_db)):
    """
    Retrieve all classrooms.
    """
    return classroom_service.list_classrooms(db)


@router.get("/{classroom_id}", response_model=ClassroomOut)
def get_classroom_route(classroom_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a classroom by its ID.
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
    Update an existing classroom.
    """
    updated = classroom_service.modify_classroom(db, classroom_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return updated


@router.delete("/{classroom_id}")
def delete_classroom_route(classroom_id: int, db: Session = Depends(get_db)):
    """
    Delete a classroom by its ID.
    """
    if not classroom_service.remove_classroom(db, classroom_id):
        raise HTTPException(status_code=404, detail="Classroom not found")
    return {"message": "Classroom deleted successfully"}
