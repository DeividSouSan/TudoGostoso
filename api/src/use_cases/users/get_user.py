from uuid import UUID

from fastapi import Depends

from ...models.users import User
from ...repositories.user_repository import UserRepository


class GetUser:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, id_user: UUID | str) -> User | None:
        if isinstance(id_user, str):
            id_user = UUID(id_user)

        user = self._repository.get_by_id(id_user)

        return user
