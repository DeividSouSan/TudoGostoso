from uuid import UUID

from ...contracts.user_repository import IUserRepository
from ...models.users import User


class GetUser:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def execute(self, id_user: UUID) -> User | None:
        return self._repository.get_by_id(id_user)
