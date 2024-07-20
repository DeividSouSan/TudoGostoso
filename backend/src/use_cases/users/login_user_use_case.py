from uuid import UUID

from fastapi import Depends

from ...dtos.user_login_dto import UserLoginDTO
from ...models.user import User
from ...repositories.user_repository import UserRepository
from ...utils.password_hasher import PasswordHasher


class LoginUserUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, user: UserLoginDTO) -> str:
        if user_db := self._repository.get_by_email(user.email):
            if PasswordHasher.verify(user.password, user_db.password_hash):
                return "Token"
            else:
                raise Exception("Senha errada")
        else:
            raise Exception("Email não existe")
    