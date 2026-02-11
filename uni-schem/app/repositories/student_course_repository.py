from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student_course import StudentCourse
from fastapi import HTTPException, status
from app.models.course import Course
from app.models.student import Student


def create_student_course(db: Session, relation: StudentCourse) -> StudentCourse:
    """
    Adds a new student-course enrollment to the database after validating no duplicates.

    Args:
        db (Session): SQLAlchemy session object.
        relation (StudentCourse): The enrollment to insert.

    Returns:
        StudentCourse: The newly created enrollment.

    Raises:
        HTTPException: If the student is already enrolled in the course.
    """
    student = db.query(Student).filter(
        Student.student_id == relation.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(Course).filter(
        Course.course_id == relation.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing_relation = db.query(StudentCourse).filter(
        StudentCourse.student_id == relation.student_id,
        StudentCourse.course_id == relation.course_id
    ).first()

    if existing_relation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course."
        )

    try:
        db.add(relation)
        db.commit()
        db.refresh(relation)
        return relation
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the student in the course."
        ) from exc


def get_student_course_by_id(db: Session, relation_id: int) -> Optional[StudentCourse]:
    """
    Retrieves an enrollment by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): The ID of the enrollment.

    Returns:
        Optional[StudentCourse]: The enrollment if found, else None.
    """
    return db.query(StudentCourse).filter(StudentCourse.student_course_id == relation_id).first()


def get_all_student_courses(db: Session) -> List[StudentCourse]:
    """
    Retrieves all student-course enrollments.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[StudentCourse]: List of all enrollments.
    """
    return db.query(StudentCourse).all()


def get_students_by_course_id(db: Session, course_id: int) -> List[StudentCourse]:
    """
    Retrieves all students enrolled in a specific course by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        course_id (int): The ID of the course.

    Returns:
        List[StudentCourse]: List of enrollments for the specified course.
    """
    return db.query(StudentCourse).filter(StudentCourse.course_id == course_id).all()


def get_student_course_by_student_and_course(db: Session, student_id: int, course_id: int) -> Optional[StudentCourse]:
    """
    Retrieves the student-course relationship based on student_id and course_id.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): The ID of the student.
        course_id (int): The ID of the course.

    Returns:
        Optional[StudentCourse]: The student-course relationship if found, else None.
    """
    return db.query(StudentCourse).filter(
        StudentCourse.student_id == student_id,
        StudentCourse.course_id == course_id
    ).first()


def get_courses_by_student_id(db: Session, student_id: int) -> List[StudentCourse]:
    """
    Retrieves all courses a specific student is enrolled in by their student ID.

    Args:
        db (Session): SQLAlchemy session object.
        student_id (int): The ID of the student.

    Returns:
        List[StudentCourse]: List of enrollments for the specified student.
    """
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).all()


def delete_student_course(db: Session, relation_id: int) -> bool:
    """
    Deletes a student-course enrollment by its ID and ensures cascading deletion of related records.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): The ID of the student-course relationship to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    relation = get_student_course_by_id(db, relation_id)
    if not relation:
        return False

    db.delete(relation)
    db.commit()
    return True
