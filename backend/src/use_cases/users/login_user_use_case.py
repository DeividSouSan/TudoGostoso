from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ...dtos.user_login_dto import UserLoginDTO
from ...models.users import User
from ...repositories.user_repository import UserRepository
from ...utils.password_hasher import PasswordHasher
from ...utils.token_generator import TokenGenerator


class LoginUserUseCase:
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
        token_handler: TokenGenerator = Depends(TokenGenerator),
    ):
        self._repository = repository
        self._token_handler = token_handler

    def execute(self, user: UserLoginDTO) -> str:
        user_db = self._repository.get_by_email(user.email)

        if user_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with email not found.",
            )

        if not PasswordHasher.verify(user.password, user_db.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password."
            )

        token = self._token_handler.generate(
            {"email": user_db.email, "role": jsonable_encoder(user_db.role)}
        )

        return token
