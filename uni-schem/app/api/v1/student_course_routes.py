from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.student_course import (
    StudentCourseCreate,
    StudentCourseUpdate,
    StudentCourseOut,
)
from app.services import student_course_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=StudentCourseOut)
def create_student_course_route(
    data: StudentCourseCreate, db: Session = Depends(get_db)
):
    """
    Creates a new enrollment record linking a student to a course.

    Args:
        data (StudentCourseCreate): The enrollment details to register.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        StudentCourseOut: The newly created student-course enrollment record.

    Raises:
        HTTPException: If validation fails, returns 400 Bad Request with the error message.
    """
    try:
        return student_course_service.register_student_course(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[StudentCourseOut])
def list_student_courses_route(db: Session = Depends(get_db)):
    """
    Retrieves all student-course enrollment records from the database.

    Args:
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[StudentCourseOut]: A list of all registered student-course enrollments.
    """
    return student_course_service.list_student_courses(db)


@router.get("/{relation_id}", response_model=StudentCourseOut)
def get_student_course_route(relation_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single student-course enrollment record by its ID.

    Args:
        relation_id (int): The unique identifier of the student-course enrollment.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        StudentCourseOut: The requested enrollment record.

    Raises:
        HTTPException: If the enrollment is not found, returns a 404 Not Found error.
    """
    relation = student_course_service.get_student_course(db, relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return relation


@router.put("/{relation_id}", response_model=StudentCourseOut)
def update_student_course_route(
    relation_id: int, updates: StudentCourseUpdate, db: Session = Depends(get_db)
):
    """
    Updates an existing student-course enrollment by its ID.

    Args:
        relation_id (int): The unique identifier of the enrollment to update.
        updates (StudentCourseUpdate): The data containing fields to update.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        StudentCourseOut: The updated enrollment record.

    Raises:
        HTTPException: If the enrollment is not found, returns a 404 Not Found error.
    """
    updated = student_course_service.modify_student_course(
        db, relation_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return updated


@router.delete("/{relation_id}")
def delete_student_course_route(relation_id: int, db: Session = Depends(get_db)):
    """
    Deletes a student-course enrollment by its ID.

    Args:
        relation_id (int): The unique identifier of the enrollment to delete.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        dict: A message confirming successful deletion.

    Raises:
        HTTPException: If the enrollment is not found, returns a 404 Not Found error.
    """
    if not student_course_service.remove_student_course(db, relation_id):
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Enrollment deleted successfully"}
