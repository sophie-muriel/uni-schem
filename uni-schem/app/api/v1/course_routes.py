from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.services import course_service
from app.db.database import SessionLocal

router = APIRouter()


def get_db():
    """
    Dependency that provides a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CourseOut)
def create_course_route(course: CourseCreate, db: Session = Depends(get_db)):
    """
    Create a new course.
    """
    try:
        return course_service.register_course(db, course)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CourseOut])
def list_courses_route(db: Session = Depends(get_db)):
    """
    Retrieve all courses.
    """
    return course_service.list_courses(db)


@router.get("/{course_id}", response_model=CourseOut)
def get_course_route(course_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a course by its ID.
    """
    course = course_service.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseOut)
def update_course_route(
    course_id: int, updates: CourseUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing course.
    """
    updated = course_service.modify_course(db, course_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


@router.delete("/{course_id}")
def delete_course_route(course_id: int, db: Session = Depends(get_db)):
    """
    Delete a course by its ID.
    """
    if not course_service.remove_course(db, course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
