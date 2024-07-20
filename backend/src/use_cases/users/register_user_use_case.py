from uuid import UUID

from fastapi import Depends

from ...dtos.user_register_dto import UserRegisterDTO
from ...dtos.user_dto import UserDTO
from ...models.user import User
from ...repositories.user_repository import UserRepository
from ...utils.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, user: UserRegisterDTO) -> None:
        new_user = self._generate_user(user)
        self._repository.add(new_user)

    def _generate_user(self, user: UserRegisterDTO) -> User:
        return User(
            username=user.username,
            fullname=user.fullname,
            password_hash=PasswordHasher.hash(user.password),
            email=user.email
        )
