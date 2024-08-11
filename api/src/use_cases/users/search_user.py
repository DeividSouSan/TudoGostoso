from ...contracts.user_repository import IUserRepository
from ...models.users import User


class SearchUser:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(self, username: str) -> list[User]:
        return self._repository.search(username)
