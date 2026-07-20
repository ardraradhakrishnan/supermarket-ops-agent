from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.database.base import Base

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@contextmanager
def get_db():
    """
    Provide a transactional database session.
    """

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)