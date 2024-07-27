from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.users import User
from ..utils.deps import get_db
from ..utils.exceptions import UserAlreadyExistsError


class UserRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self.__session = session

    def add(self, user: User) -> None:
        if self.get_by_email(user.email) or self.get_by_username(user.username):
            raise UserAlreadyExistsError()

        self.__session.add(user)
        self.__session.commit()

    def all(self) -> list[User]:
        return self.__session.query(User).all()

    def get_by_id(self, id: UUID) -> User | None:
        return self.__session.query(User).filter(User.id_user == id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.__session.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User | None:
        return self.__session.query(User).filter(User.email == username).first()
