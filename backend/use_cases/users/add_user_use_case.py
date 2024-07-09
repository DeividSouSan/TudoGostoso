
from uuid import UUID
from dtos.register_user_dto import RegisterUserDTO
from models.user import User
from dtos.user_dto import UserDTO
from repository.user_repository import UserRepository


class AddUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, user: RegisterUserDTO) -> UserDTO:
        
        new_user = User(
            username=user.username,
            fullname=user.fullname,
            password_hash=user.password_1,
            email=user.email,
        )   
        
        self._repository.add_user(new_user)

        return UserDTO(new_user)
