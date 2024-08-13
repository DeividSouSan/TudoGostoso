import random

from ...contracts.email_sender import IEmailSender
from ...contracts.password_hasher import IPasswordHasher
from ...contracts.user_repository import IUserRepository
from ...dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ...models.users import User
from ...utils.exceptions import UserAlreadyExists


class RegisterUser:
    def __init__(
        self,
        repository: IUserRepository = None,
        password_hasher: IPasswordHasher = None,
        email_sender: IEmailSender = None,
    ) -> None:

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
            activation_code=random.randint(100000, 999999),  # Poderia ser uma classe
        )

        self._repository.add(new_user)

        self._email_sender.send_activation_code(
            email_address=new_user.email, activation_code=new_user.activation_code
        )
