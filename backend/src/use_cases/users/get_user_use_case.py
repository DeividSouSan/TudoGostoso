from uuid import UUID

from src.dtos.user_dto import UserDTO
from src.repositories.user_repository import UserRepository


class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, id_user: UUID) -> UserDTO:
        user = self._repository.get_user(id_user)
        user_dto = UserDTO(user)

        return user_dto
