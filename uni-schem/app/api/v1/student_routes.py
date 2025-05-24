from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.services import student_service
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=StudentOut)
def create_student_route(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Creates a new student record.

    Args:
        student (StudentCreate): The data for the student to be created.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        StudentOut: The newly created student record.

    Raises:
        HTTPException: If the input data is invalid, returns a 400 Bad Request error.
    """
    try:
        return student_service.register_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/", response_model=List[StudentOut])
def list_students_route(db: Session = Depends(get_db)):
    """
    Retrieves all student records.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[StudentOut]: A list of all registered students.
    """
    return student_service.list_students(db)

@router.get("/{student_id}", response_model=StudentOut)
def get_student_route(student_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a student record by ID.

    Args:
        student_id (int): Unique identifier of the student.
        db (Session): Database session dependency (injected).

    Returns:
        StudentOut: The student data if found.

    Raises:
        HTTPException: If no student exists with the given ID, returns a 404 Not Found error.
    """
    student = student_service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/dni/{dni}", response_model=StudentOut)
def get_student_by_dni_route(dni: str, db: Session = Depends(get_db)):
    """
    Retrieves a student record by their DNI (document number).

    Args:
        dni (str): The DNI (document number) of the student.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        StudentOut: The student data if found.

    Raises:
        HTTPException: If no student exists with the given DNI, returns a 404 Not Found error.
    """
    student = student_service.get_student_by_dni(db, dni)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentOut)
def update_student_route(student_id: int, updates: StudentUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing student record.

    Args:
        student_id (int): The unique ID of the student to update.
        updates (StudentUpdate): The updated student data.
        db (Session): The database session dependency.

    Returns:
        StudentOut: The updated student data.

    Raises:
        HTTPException: If the student is not found, returns a 404 Not Found error.
    """
    updated_student = student_service.modify_student(db, student_id, updates)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/{student_id}")
def delete_student_route(student_id: int, db: Session = Depends(get_db)):
    """
    Delete a student by their ID.

    Args:
        student_id (int): The ID of the student to delete.
        db (Session): Database session (injected).

    Returns:
        dict: Deletion confirmation message.

    Raises:
        HTTPException: If the student is not found, returns a 404 Not Found error.
    """
    if not student_service.remove_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
