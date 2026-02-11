from .database import SessionLocal
from fastapi import HTTPException, status  # <-- ¡Importa esto!


def get_db():
    """
    Provides a SQLAlchemy database session to FastAPI endpoints.

    This dependency function creates a new database session,
    yields it for use in a request, and ensures the session
    is properly closed after the request completes. It also
    handles database transaction rollbacks in case of errors.

    Yields:
        Session: A SQLAlchemy database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected server error occurred: {e}"
            )
    finally:
        db.close()
