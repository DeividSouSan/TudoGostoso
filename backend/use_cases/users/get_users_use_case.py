
from backend.dtos.user_dto import GetUserDTO
from repository.user_repository import UserRepository


class GetUsersUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self):
        users = self._repository.get_users()
        users_dto = map(GetUserDTO, users)

        return users_dto
