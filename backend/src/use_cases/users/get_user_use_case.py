from uuid import UUID

from fastapi import Depends

from ...dtos.user_dto import UserDTO
from ...repositories.user_repository import UserRepository


class GetUserUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self, id_user: UUID) -> UserDTO:
        user = self._repository.get_user(id_user)
        
        if user is None:
            raise Exception("oi")
        
        return UserDTO(user)
        
        
