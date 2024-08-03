from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ...dtos.user.user_login_request_dto import UserLoginRequestDTO
from ...repositories.user_repository import UserRepository
from ...utils.password_hasher import PasswordHasher
from ...utils.token_generator import TokenGenerator
from ...utils.exceptions import UserNotFound, WrongPassword


class LoginUserUseCase:
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
        token_handler: TokenGenerator = Depends(TokenGenerator),
    ):
        self._repository = repository
        self._token_handler = token_handler

    def execute(self, user: UserLoginRequestDTO) -> str:
        user_db = self._repository.get_by_email(user.email)

        if user_db is None:
            raise UserNotFound()

        if not PasswordHasher.verify(user.password, user_db.password_hash):
            raise WrongPassword()

        return self._token_handler.generate(
            {
                "id": jsonable_encoder(user_db.id_user),
                "role": jsonable_encoder(user_db.role),
            }
        )
