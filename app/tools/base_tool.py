from sqlalchemy.orm import Session

from app.database.database import SessionLocal


class BaseTool:
    """
    Base class for all Google ADK tools.
    """

    def __enter__(self):
        self.db: Session = SessionLocal()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.db.close()