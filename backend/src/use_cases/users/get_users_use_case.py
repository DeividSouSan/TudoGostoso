from uuid import UUID

from fastapi import Depends

from ...models.users import User
from ...repositories.user_repository import UserRepository


class GetUsersUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, id_user: UUID) -> list[User]:
        if id_user:
            user = self._repository.get_by_id(id_user)
            return [] if user is None else [user]

        return self._repository.all()
