from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.student_course import (
    StudentCourseCreate,
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


@router.get("/course/{course_id}", response_model=List[StudentCourseOut])
def get_students_by_course_route(course_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all students enrolled in a specific course by course ID.

    Args:
        course_id (int): The unique ID of the course.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[StudentCourseOut]: A list of students enrolled in the given course.

    Raises:
        HTTPException: If no students are found for the course, returns a 404 Not Found error.
    """
    relations = student_course_service.get_students_by_course_id(db, course_id)
    if not relations:
        raise HTTPException(
            status_code=404, detail="No students found for this course")
    return relations


@router.get("/student/{student_id}", response_model=List[StudentCourseOut])
def get_courses_by_student_route(student_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all courses a specific student is enrolled in by student ID.

    Args:
        student_id (int): The unique ID of the student.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[StudentCourseOut]: A list of courses the student is enrolled in.

    Raises:
        HTTPException: If no courses are found for the student, returns a 404 Not Found error.
    """
    relations = student_course_service.get_courses_by_student_id(
        db, student_id)
    if not relations:
        raise HTTPException(
            status_code=404, detail="No courses found for this student")
    return relations


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
