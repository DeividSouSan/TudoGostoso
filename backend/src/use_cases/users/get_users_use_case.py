from ...dtos.user_dto import UserDTO
from ...repositories.user_repository import UserRepository
from fastapi import Depends

class GetUsersUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self) -> list[UserDTO]:
        users = self._repository.get_users()

        users_dto = map(UserDTO, users)

        return users_dto
