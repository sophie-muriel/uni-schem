from sqlalchemy.orm import Session
from app.models.student_course import StudentCourse
from typing import List, Optional


def create_student_course(db: Session, relation: StudentCourse) -> StudentCourse:
    """
    Adds a new student-course enrollment to the database.

    Args:
        db (Session): SQLAlchemy session object.
        relation (StudentCourse): The enrollment to insert.

    Returns:
        StudentCourse: The newly created enrollment.
    """
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


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


def update_student_course(db: Session, relation_id: int, updates: dict) -> Optional[StudentCourse]:
    """
    Updates an existing enrollment.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): ID of the enrollment.
        updates (dict): Fields to update.

    Returns:
        Optional[StudentCourse]: The updated enrollment or None if not found.
    """
    relation = get_student_course_by_id(db, relation_id)
    if not relation:
        return None

    for key, value in updates.items():
        setattr(relation, key, value)

    db.commit()
    db.refresh(relation)
    return relation


def delete_student_course(db: Session, relation_id: int) -> bool:
    """
    Deletes an enrollment by its ID.

    Args:
        db (Session): SQLAlchemy session object.
        relation_id (int): ID of the enrollment to delete.

    Returns:
        bool: True if deleted, False otherwise.
    """
    relation = get_student_course_by_id(db, relation_id)
    if not relation:
        return False

    db.delete(relation)
    db.commit()
    return True