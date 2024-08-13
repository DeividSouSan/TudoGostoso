from uuid import UUID

from ...contracts.user_repository import IUserRepository
from ...utils.exceptions import UnauthorizedAccountDelete, UserNotFound


class DeleteUser:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    def execute(self, user_id: UUID, current_user: dict) -> None:
        user = self._repository.get_by_id(user_id)

        if not user:
            raise UserNotFound()

        if current_user["role"] == "user":
            TARGET_USER_ID = user.user_id
            CURRENT_USER_ID = UUID(current_user["id"])

            if TARGET_USER_ID != CURRENT_USER_ID:
                raise UnauthorizedAccountDelete()

        self._repository.delete(user)
