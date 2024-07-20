from typing import Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session
from ..models.user import User


class UserRepository:
    def __init__(self):
        from ..db.connection import engine

        self.__engine = engine

    def add(self, user: User) -> None:
        with Session(self.__engine) as session:
            session.add(user)
            session.commit()

    def all(self) -> list[User]:
        with Session(self.__engine) as session:
            return session.query(User).all()

    def get_by_id(self, id: UUID) -> User | None:
        with Session(self.__engine) as session:
            return session.query(User).filter(User.id_user == id).first()

    def get_by_email(self, email: str) -> User | None:
        with Session(self.__engine) as session:
            return session.query(User).filter(User.email == email).first()
