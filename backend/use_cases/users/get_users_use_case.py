
from backend.dtos.user_dto import UserDTO
from repository.user_repository import UserRepository


class GetUsersUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self) -> UserDTO:
        users = self._repository.get_users()
        
        users_dto = map(UserDTO, users)

        return users_dto
