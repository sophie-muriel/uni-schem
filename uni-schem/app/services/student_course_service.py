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
        data (StudentCourseCreate): Data for the new enrollment, including student ID and course ID.

    Returns:
        StudentCourse: The newly created student-course relationship.
    """
    new_relation = StudentCourse(
        student_id=data.student_id,
        course_id=data.course_id
    )
    return student_course_repository.create_student_course(db, new_relation)


def get_student_course(db: Session, relation_id: int) -> Optional[StudentCourse]:
    """
    Retrieves a specific student-course enrollment by its unique ID.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): The ID of the student-course relation.

    Returns:
        Optional[StudentCourse]: The enrollment if found, otherwise None.
    """
    return student_course_repository.get_student_course_by_id(db, relation_id)


def list_student_courses(db: Session) -> List[StudentCourse]:
    """
    Retrieves all student-course enrollments from the database.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[StudentCourse]: A list of all student-course relationships.
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
    Deletes a student-course enrollment by its unique ID.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): The ID of the student-course relation to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    return student_course_repository.delete_student_course(db, relation_id)
