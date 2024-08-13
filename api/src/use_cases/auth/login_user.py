from ...contracts.password_hasher import IPasswordHasher
from ...contracts.token_generator import ITokenGenerator
from ...contracts.user_repository import IUserRepository
from ...dtos.user.user_login_request_dto import UserLoginRequestDTO
from ...utils.exceptions import UserNotFound, WrongPassword


class LoginUser:
    def __init__(
        self,
        repository: IUserRepository,
        token_handler: ITokenGenerator,
        password_hasher: IPasswordHasher,
    ):
        self._repository = repository
        self._token_handler = token_handler
        self._password_hasher = password_hasher

    def execute(self, user: UserLoginRequestDTO) -> str:
        user_db = self._repository.get_by_email(user.email)

        if user_db is None:
            raise UserNotFound()

        if not self._password_hasher.verify(user.password, user_db.password_hash):
            raise WrongPassword()

        return self._token_handler.generate(
            {
                "id": str(user_db.id_user),
                "role": str(user_db.role),
            }
        )
