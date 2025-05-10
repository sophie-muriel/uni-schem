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
    Create a new student record.

    Args:
        student (StudentCreate): The student data to be created.
        db (Session): Database session (injected).

    Returns:
        StudentOut: The created student.
    """
    try:
        return student_service.register_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[StudentOut])
def list_students_route(db: Session = Depends(get_db)):
    """
    Retrieve all students from the database.

    Args:
        db (Session): Database session (injected).

    Returns:
        List[StudentOut]: A list of all students.
    """
    return student_service.list_students(db)


@router.get("/{student_id}", response_model=StudentOut)
def get_student_route(student_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single student by their ID.

    Args:
        student_id (int): The student's unique identifier.
        db (Session): Database session (injected).

    Returns:
        StudentOut: The matching student if found.

    Raises:
        HTTPException: If student is not found.
    """
    student = student_service.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentOut)
def update_student_route(
    student_id: int, updates: StudentUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing student's information.

    Args:
        student_id (int): The ID of the student to update.
        updates (StudentUpdate): The data to update.
        db (Session): Database session (injected).

    Returns:
        StudentOut: The updated student.

    Raises:
        HTTPException: If student is not found.
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
        HTTPException: If student is not found.
    """
    if not student_service.remove_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
