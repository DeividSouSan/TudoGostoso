from sre_constants import CH_UNICODE
from uuid import UUID

from fastapi import Depends

from api.src.repositories.user_repository import UserRepository
from api.src.utils.exceptions import UnauthorizedAccountDelete, UserNotFound


class DeleteUser:
    def __init__(self, repository: UserRepository = Depends(UserRepository)) -> None:
        self._repository = repository

    def execute(self, user_id: UUID, current_user_token: dict) -> None:
        user = self._repository.get_by_id(user_id)

        if not user:
            raise UserNotFound()

        if current_user_token["role"] == "user":
            TARGET_USER_ID = user.user_id
            CURRENT_USER_ID = UUID(current_user_token["id"])

            if TARGET_USER_ID != CURRENT_USER_ID:
                raise UnauthorizedAccountDelete()

        self._repository.delete(user)
