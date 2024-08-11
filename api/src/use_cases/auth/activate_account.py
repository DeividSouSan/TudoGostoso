
from ...contracts.user_repository import IUserRepository
from ...repositories.user_repository import UserRepository
from ...utils.exceptions import AccountAlreadyActive


class ActivateAccount:
    def __init__(self, respository: IUserRepository):
        self._repository = respository

    def execute(self, code: str) -> None:
        user = self._repository.get_by_activation_code(code)

        if user is None:
            raise AccountAlreadyActive()

        self._repository.activate_account(user)
