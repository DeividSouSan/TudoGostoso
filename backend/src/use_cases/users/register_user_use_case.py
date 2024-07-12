from uuid import UUID

from backend.src.dtos.user_register_dto import UserRegisterDTO
from src.dtos.user_dto import UserDTO
from src.models.user import User
from src.repositories.user_repository import UserRepository


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, user: UserRegisterDTO) -> None:

        new_user = self._generate_user(user)

        self._repository.add_user(new_user)

    def _generate_user(self, user: User) -> User:
        return User(
            username=user.username,
            fullname=user.fullname,
            password_hash=user.password, # ! Fazer o hash aqui
            email=user.email
        )