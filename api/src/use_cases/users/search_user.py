from ...models.users import User
from ...repositories.user_repository import UserRepository
from fastapi import Depends

class SearchUser:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    def execute(self, username: str) -> list[User]:
        return self.user_repository.search(username)
