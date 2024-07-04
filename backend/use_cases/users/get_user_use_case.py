
from uuid import UUID
from dtos.get_user_dto import GetUserDTO
from repository.user_repository import UserRepository


class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, id_user: UUID):
        user = self._repository.get_user(id_user)
        user_dto = GetUserDTO(user)

        return user_dto
