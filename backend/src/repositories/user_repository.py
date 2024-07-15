from uuid import UUID

from sqlalchemy.orm import Session
from src.models.user import User


class UserRepository:
    def __init__(self):
        from src.db.connection import engine

        self.__engine = engine

    def add_user(self, user: User) -> None:
        with Session(self.__engine) as session:
            session.add(user)
            session.commit()

    def get_users(self) -> list[User]:
        with Session(self.__engine) as session:
            users = session.query(User).all()

            return users

    def get_user(self, id_user: UUID) -> User:
        with Session(self.__engine) as session:
            user = session.query(User).filter(User.id_user == id_user).first()

            return user

    def get_by_email(self, user_email: str) -> User:
        with Session(self.__engine) as session:
            return session.query(User).filter(User.email == user_email).first()
            