from uuid import UUID

from ...contracts.user_repository import IUserRepository
from ...models.users import User


class GetAllUsers:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(self) -> list[User]:
        return self._repository.all()
