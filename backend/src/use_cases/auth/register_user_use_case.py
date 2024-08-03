import random

from fastapi import Depends, HTTPException, status

from ...dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ...models.users import User
from ...repositories.user_repository import UserRepository
from ...utils.activation_code_email_sender import ActivationCodeEmailSender
from ...utils.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, user: UserRegisterRequestDTO) -> None:
        EMAIL_ALREADY_EXISTS = bool(self._repository.get_by_email(user.email))
        USERNAME_ALREADY_EXISTS = bool(self._repository.get_by_username(user.username))

        if EMAIL_ALREADY_EXISTS or USERNAME_ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with given email or username already exists.",
            )

        new_user = User(
            username=user.username,
            fullname=user.fullname,
            password_hash=PasswordHasher.hash(user.password),
            email=user.email,
            activation_code=random.randint(100000, 999999),
        )

        self._repository.add(new_user)

        ActivationCodeEmailSender.send_activation_code(
            email_address=new_user.email, activation_code=new_user.activation_code
        )