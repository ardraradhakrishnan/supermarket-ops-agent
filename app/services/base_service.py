from sqlalchemy import ScalarResult
from sqlalchemy.orm import Session


class BaseService:
    """
    Base service providing common database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def add(self, instance):
        self.db.add(instance)

    def add_all(self, instances):
        self.db.add_all(instances)

    def remove(self, instance):
        self.db.delete(instance)

    def flush(self):
        """
        Flush pending SQL statements without committing.
        """
        self.db.flush()

    def refresh(self, instance):
        self.db.refresh(instance)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def scalar(self, statement):
        return self.db.scalar(statement)

    def scalars(self, statement):
        return list(self.db.scalars(statement))

    def execute(self, statement):
        return self.db.execute(statement).all()