from uuid import UUID

from fastapi import APIRouter

from dtos.register_user_dto import RegisterUserDTO
from dtos.get_user_dto import GetUserDTO
from models.user import User
from repository.user_repository import UserRepository
from use_cases.users.get_user_use_case import GetUserUseCase
from use_cases.users.get_users_use_case import GetUsersUseCase

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get("")
async def get_users() -> list[GetUserDTO]:
    repository = UserRepository()

    use_case = GetUsersUseCase(repository)
    users = use_case.execute()

    return users


@user_router.get("/{id_user:uuid}")
async def get_user(id_user: UUID) -> GetUserDTO:
    repository = UserRepository()

    use_case = GetUserUseCase(repository)
    user = use_case.execute(id_user)

    return user


@user_router.post("")
async def add_user(user: RegisterUserDTO):
    repository = UserRepository()

    new_user = User(
        username=user.username,
        fullname=user.fullname,
        password_hash=user.password_1,
        email=user.email,
    )

    repository.add_user(new_user)

    return user


@user_router.put("/{user_id}")
async def update_recipe(user_id: int):
    return {"response": f"updated recipe {user_id}"}


@user_router.delete("/{user_id}")
async def delete_recipe(user_id: int):
    return {"response": f"deleted recipe {user_id}"}
