from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.student_course import StudentCourse
from app.schemas.student_course import StudentCourseCreate
from app.repositories import student_course_repository, student_repository, course_repository


def register_student_course(db: Session, data: StudentCourseCreate) -> StudentCourse:
    """
    Registers a new student-course enrollment after validating the student and course existence,
    and checking for duplicate enrollments.

    Args:
        db (Session): SQLAlchemy session object.
        data (StudentCourseCreate): The enrollment details.

    Returns:
        StudentCourse: The created student-course enrollment.
    """
    student = student_repository.get_student_by_id(db, data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = course_repository.get_course_by_id(db, data.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing_relation = student_course_repository.get_student_course_by_student_and_course(
        db, data.student_id, data.course_id
    )
    if existing_relation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course."
        )

    new_relation = StudentCourse(
        student_id=data.student_id,
        course_id=data.course_id
    )

    return student_course_repository.create_student_course(db, new_relation)



def get_student_course(db: Session, relation_id: int) -> Optional[StudentCourse]:
    """
    Retrieves a student-course enrollment by its unique ID.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): The ID of the student-course relation to retrieve.

    Returns:
        Optional[StudentCourse]: The enrollment object if found, otherwise None.
    """
    return student_course_repository.get_student_course_by_id(db, relation_id)


def list_student_courses(db: Session) -> List[StudentCourse]:
    """
    Retrieves all existing student-course enrollments.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[StudentCourse]: A list of all student-course relationships stored in the database.
    """
    return student_course_repository.get_all_student_courses(db)


def get_students_by_course_id(db: Session, course_id: int) -> List[StudentCourse]:
    """
    Retrieves all students enrolled in a specific course.

    Args:
        db (Session): SQLAlchemy session object.
        course_id (int): The ID of the course.

    Returns:
        List[StudentCourse]: List of enrollments for the course.
    """
    return student_course_repository.get_students_by_course_id(db, course_id)


def get_courses_by_student_id(db: Session, student_id: int) -> List[StudentCourse]:
    """
    Retrieves all courses a specific student is enrolled in.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): The ID of the student.

    Returns:
        List[StudentCourse]: List of enrollments for the student.
    """
    return student_course_repository.get_courses_by_student_id(db, student_id)


def remove_student_course(db: Session, relation_id: int) -> bool:
    """
    Deletes a student-course enrollment by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): The ID of the student-course relationship to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    return student_course_repository.delete_student_course(db, relation_id)
