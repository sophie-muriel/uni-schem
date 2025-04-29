from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.student_course import (
    StudentCourseCreate,
    StudentCourseUpdate,
    StudentCourseOut,
)
from app.services import student_course_service
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


@router.post("/", response_model=StudentCourseOut)
def create_student_course_route(
    data: StudentCourseCreate, db: Session = Depends(get_db)
):
    """
    Create a new student-course enrollment.
    """
    try:
        return student_course_service.register_student_course(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StudentCourseOut])
def list_student_courses_route(db: Session = Depends(get_db)):
    """
    Retrieve all student-course enrollments.
    """
    return student_course_service.list_student_courses(db)


@router.get("/{relation_id}", response_model=StudentCourseOut)
def get_student_course_route(relation_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a student-course enrollment by ID.
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
    Update an existing student-course enrollment.
    """
    updated = student_course_service.modify_student_course(db, relation_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return updated


@router.delete("/{relation_id}")
def delete_student_course_route(relation_id: int, db: Session = Depends(get_db)):
    """
    Delete a student-course enrollment by ID.
    """
    if not student_course_service.remove_student_course(db, relation_id):
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Enrollment deleted successfully"}
