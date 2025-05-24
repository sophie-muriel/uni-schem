from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.services import course_service
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=CourseOut)
def create_course_route(course: CourseCreate, db: Session = Depends(get_db)):
    """
    Creates a new course entry.

    Args:
        course (CourseCreate): The course information to be registered.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        CourseOut: The newly created course record.

    Raises:
        HTTPException: If a ValueError occurs during registration, returns a 400 Bad Request
        with the corresponding error message.
    """
    try:
        # Verificar si el nombre del curso ya existe
        existing_course_by_name = db.query(Course).filter(
            Course.name == course.name).first()
        if existing_course_by_name:
            raise HTTPException(
                status_code=400, detail="Course with this name already exists.")

        # Verificar si el código del curso ya existe
        existing_course_by_code = db.query(Course).filter(
            Course.code == course.code).first()
        if existing_course_by_code:
            raise HTTPException(
                status_code=400, detail="Course with this code already exists.")

        return course_service.register_course(db, course)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=List[CourseOut])
def list_courses_route(db: Session = Depends(get_db)):
    """
    Retrieves all course entries from the database.

    Args:
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[CourseOut]: A list of all registered courses.
    """
    return course_service.list_courses(db)


@router.get("/name/{course_name}", response_model=CourseOut)
def get_course_by_name_route(course_name: str, db: Session = Depends(get_db)):
    """
    Retrieves a course by its name.

    Args:
        course_name (str): The name of the course.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        CourseOut: The requested course record.

    Raises:
        HTTPException: If the course is not found, returns a 404 Not Found error.
    """
    course = course_service.get_course_by_name(db, course_name)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/professor/{professor_id}", response_model=List[CourseOut])
def get_courses_by_professor_id_route(professor_id: int, db: Session = Depends(get_db)):
    """
    Retrieves courses by professor ID.

    Args:
        professor_id (int): The unique identifier of the professor.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        List[CourseOut]: A list of courses assigned to the professor.

    Raises:
        HTTPException: If no courses are found for the professor, returns a 404 Not Found error.
    """
    courses = course_service.get_courses_by_professor_id(db, professor_id)
    if not courses:
        raise HTTPException(
            status_code=404, detail="No courses found for this professor")
    return courses


@router.get("/{course_id}", response_model=CourseOut)
def get_course_route(course_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a course entry by its unique ID.

    Args:
        course_id (int): The unique identifier of the course.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        CourseOut: The requested course record.

    Raises:
        HTTPException: If the course is not found, returns a 404 Not Found error.
    """
    course = course_service.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseOut)
def update_course_route(course_id: int, updates: CourseUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing course entry by its ID.

    Args:
        course_id (int): The unique identifier of the course to update.
        updates (CourseUpdate): The data containing the fields to be updated.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        CourseOut: The updated course record.

    Raises:
        HTTPException: If the course is not found, returns a 404 Not Found error.
    """
    updated = course_service.modify_course(db, course_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


@router.delete("/{course_id}")
def delete_course_route(course_id: int, db: Session = Depends(get_db)):
    """
    Deletes a course entry by its ID.

    Args:
        course_id (int): The unique identifier of the course to delete.
        db (Session): SQLAlchemy session, injected by FastAPI.

    Returns:
        dict: A confirmation message indicating successful deletion.

    Raises:
        HTTPException: If the course is not found, returns a 404 Not Found error.
    """
    if not course_service.remove_course(db, course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
