from typing import Optional, TypeVar, Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.deps import get_db

class UserRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self.__session = session

    def add(self, user: User) -> None:
            self.__session.add(user)
            self.__session.commit()

    def all(self) -> list[User]:
        return self.__session.query(User).all()

    def get_by_id(self, id: UUID) -> User | None:
        return self.__session.query(User).filter(User.id_user == id).first()

    def get_by_email(self, email: str) -> User | None:
        return self._session.query(User).filter(User.email == email).first()
