from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from ..contracts.user_repository import IUserRepository

from ..models.users import User
from ..utils.deps import get_db


class UserRepository(IUserRepository):
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self.__session = session

    def add(self, user: User) -> None:
        self.__session.add(user)
        self.__session.commit()

    def delete(self, user: User) -> None:
        self.__session.delete(user)
        self.__session.commit

    def all(self) -> list[User]:
        return self.__session.query(User).filter(User.active).all()

    def get_by_id(self, id: UUID) -> User | None:
        return (
            self.__session.query(User)
            .filter(User.id_user == id and User.active)
            .first()
        )

    def get_by_email(self, email: str) -> User | None:
        return (
            self.__session.query(User)
            .filter(User.email == email and User.active)
            .first()
        )

    def search(self, username: str) -> list[User]:
        return (
            self.__session.query(User)
            .filter(User.username.ilike(f"%{username}%") and User.active)
            .all()
        )

    def get_by_activation_code(self, token: str) -> User | None:
        return self.__session.query(User).where(User.activation_code == token).first()

