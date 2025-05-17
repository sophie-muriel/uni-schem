# db/session.py
from .database import SessionLocal


def get_db():
    """
    Provides a SQLAlchemy database session to FastAPI endpoints.

    This dependency function creates a new database session,
    yields it for use in a request, and ensures the session
    is properly closed after the request completes.

    Yields:
        Session: A SQLAlchemy database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
