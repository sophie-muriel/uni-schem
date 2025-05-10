# db/session.py
from .database import SessionLocal


def get_db():
    """
    Provides a SQLAlchemy session to the endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
