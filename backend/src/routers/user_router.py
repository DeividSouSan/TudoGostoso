from uuid import UUID

from fastapi import APIRouter
from backend.src.dtos.user_register_dto import UserRegisterDTO
from src.dtos.user_dto import UserDTO
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.use_cases.users.register_user_use_case import RegisterUserUseCase
from src.use_cases.users.get_user_use_case import GetUserUseCase
from src.use_cases.users.get_users_use_case import GetUsersUseCase

from fastapi.responses import JSONResponse

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get("")
async def get_all() -> list[UserDTO]:
    repository = UserRepository()

    use_case = GetUsersUseCase(repository)
    users = use_case.execute()

    return users


@user_router.get("/{id_user:uuid}")
async def get(id_user: UUID) -> UserDTO:
    repository = UserRepository()

    use_case = GetUserUseCase(repository)
    user = use_case.execute(id_user)

    return {"user": user}


@user_router.post("")
async def register(user: UserRegisterDTO):
    # O que geralmente eu retorno nessa rota?
    repository = UserRepository()

    use_case = RegisterUserUseCase(repository)
    use_case.execute(user)

    return JSONResponse(status_code=200, content={"message": "user added to database"})
