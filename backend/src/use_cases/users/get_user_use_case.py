from uuid import UUID

from fastapi import Depends, HTTPException, status

from ...models.users import User
from ...repositories.user_repository import UserRepository


class GetUserUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, id_user: UUID) -> User:
        user = self._repository.get_by_id(id_user)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User with id not found."
            )

        return user
