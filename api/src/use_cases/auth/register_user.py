import random

from fastapi import Depends, HTTPException, status

from ...dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ...models.users import User
from ...repositories.user_repository import UserRepository
from ...utils.activation_code_email_sender import ActivationCodeEmailSender
from ...utils.exceptions import UserAlreadyExists
from ...utils.password_hasher import PasswordHasher


class RegisterUser:
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
        password_hasher: PasswordHasher = Depends(PasswordHasher),
        email_sender: ActivationCodeEmailSender = Depends(ActivationCodeEmailSender),
    ):
        self._repository = repository
        self._password_hasher = password_hasher
        self._email_sender = email_sender

    def execute(self, user: UserRegisterRequestDTO) -> None:
        EMAIL_ALREADY_EXISTS = bool(self._repository.get_by_email(user.email))
        USERNAME_ALREADY_EXISTS = bool(self._repository.search(user.username))

        if EMAIL_ALREADY_EXISTS or USERNAME_ALREADY_EXISTS:
            raise UserAlreadyExists()

        new_user = User(
            username=user.username,
            fullname=user.fullname,
            password_hash=self._password_hasher.hash(user.password),
            email=user.email,
            activation_code=random.randint(100000, 999999),
        )

        self._repository.add(new_user)

        self._email_sender.send_activation_code(
            email_address=new_user.email, activation_code=new_user.activation_code
        )
