from typing import Generic
from typing import Type
from typing import TypeVar
from typing import Optional

from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(
        self,
        db: Session,
        model: Type[T],
    ):
        self.db = db
        self.model = model

    # =====================================================
    # CREATE
    # =====================================================

    def add(self, obj: T) -> T:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(self, id):

        return (
            self.db.query(self.model)
            .filter(self.model.id == id)
            .first()
        )

    def get_all(self):

        return self.db.query(self.model).all()

    def count(self):

        return self.db.query(self.model).count()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, obj: T):

        self.db.delete(obj)
        self.db.commit()

    # =====================================================
    # SAVE
    # =====================================================

    def save(self):

        self.db.commit()

    def refresh(self, obj: T):

        self.db.refresh(obj)