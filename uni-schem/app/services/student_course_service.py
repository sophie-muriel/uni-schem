from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student_course import StudentCourse
from app.schemas.student_course import StudentCourseCreate
from app.repositories import student_course_repository


def register_student_course(db: Session, data: StudentCourseCreate) -> StudentCourse:
    """
    Registers a new student-course enrollment.

    Args:
        db (Session): SQLAlchemy session object.
        data (StudentCourseCreate): Data for the new enrollment.

    Returns:
        StudentCourse: The created enrollment.
    """
    new_relation = StudentCourse(
        student_id=data.student_id,
        course_id=data.course_id
    )
    return student_course_repository.create_student_course(db, new_relation)


def get_student_course(db: Session, relation_id: int) -> Optional[StudentCourse]:
    """
    Retrieves an enrollment by ID.
    """
    return student_course_repository.get_student_course_by_id(db, relation_id)


def list_student_courses(db: Session) -> List[StudentCourse]:
    """
    Retrieves all student-course enrollments.
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
    Deletes an enrollment by ID.
    """
    return student_course_repository.delete_student_course(db, relation_id)
