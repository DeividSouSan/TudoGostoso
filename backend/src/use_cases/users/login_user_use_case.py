from uuid import UUID

from src.dtos.user_register_dto import UserRegisterDTO
from src.dtos.user_login_dto import UserLoginDTO
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.utils.password_hasher import PasswordHasher


class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, user: UserLoginDTO) -> str:
        if user_db := self._repository.get_by_email(user.email):
            if PasswordHasher.verify(user.password, user_db.password_hash):
                return "Token"
            else:
                raise Exception("Senha errada")
        else:
            raise Exception("Email não existe")
    