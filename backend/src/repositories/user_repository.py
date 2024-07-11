from uuid import UUID
from models.user import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self):
        from database import engine
        self.__engine = engine

    def add_user(self, user: User):
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