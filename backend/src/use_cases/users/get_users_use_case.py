from fastapi.responses import JSONResponse
from ...dtos.user_dto import UserDTO
from ...repositories.user_repository import UserRepository
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from ...models.users import User

class GetUsersUseCase:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self._repository = repository

    def execute(self) -> list[User]:
        return self._repository.all()
        

        
