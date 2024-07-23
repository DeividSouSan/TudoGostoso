from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import JSONResponse

from ...dtos.user_login_dto import UserLoginDTO
from ...models.user import User
from ...repositories.user_repository import UserRepository
from ...utils.password_hasher import PasswordHasher
from ...utils.token_generator import TokenGenerator


class LoginUserUseCase:
    def __init__(self,
                 repository: UserRepository = Depends(UserRepository),
                 token_handler: TokenGenerator = Depends(TokenGenerator)
                 ):
        self._repository = repository
        self._token_handler = token_handler

    def execute(self, user: UserLoginDTO) -> str:
        user_db = self._repository.get_by_email(user.email)

        if user_db is None:
            return JSONResponse(
                content={"msg": "Email not found."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        if not PasswordHasher.verify(user.password, user_db.password_hash):
            return JSONResponse(
                content={"msg": "Wrong password."},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        token = self._token_handler.generate({"email": user.email})

        return JSONResponse(
                    content={"token": token},
                    status_code=status.HTTP_200_OK
                )
