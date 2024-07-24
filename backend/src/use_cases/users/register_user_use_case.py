from uuid import UUID

from fastapi import Depends, HTTPException, status

from ...dtos.user_dto import UserDTO
from ...dtos.user_register_dto import UserRegisterDTO
from ...models.users import User
from ...repositories.user_repository import UserRepository
from ...utils.exceptions import UserAlreadyExistsError
from ...utils.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, user: UserRegisterDTO) -> None:
        try:
            new_user = User(
                username=user.username,
                fullname=user.fullname,
                password_hash=PasswordHasher.hash(user.password),
                email=user.email,
            )

            self._repository.add(new_user)

        except UserAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with given email or username already exists.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred.",
            )
