from fastapi import Depends

from ...models.users import User
from ...repositories.user_repository import UserRepository


class GetUsersUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self) -> list[User]:
        return self._repository.all()
