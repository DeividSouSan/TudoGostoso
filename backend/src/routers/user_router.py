from uuid import UUID

from fastapi import APIRouter, Depends
from ..dtos.user_register_dto import UserRegisterDTO
from ..dtos.user_login_dto import UserLoginDTO
from ..dtos.user_dto import UserDTO
from ..use_cases.users.login_user_use_case import LoginUserUseCase
from ..use_cases.users.register_user_use_case import RegisterUserUseCase
from ..use_cases.users.get_user_use_case import GetUserUseCase
from ..use_cases.users.get_users_use_case import GetUsersUseCase


user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get("")
async def get_all(use_case: GetUsersUseCase = Depends(GetUsersUseCase)) -> list[UserDTO]:
    return use_case.execute()


@user_router.get("/{id_user:uuid}")
async def get(id_user: UUID, use_case: GetUserUseCase = Depends(GetUserUseCase)) -> UserDTO:
    return use_case.execute(id_user)


@user_router.post("")
async def register(user: UserRegisterDTO, use_case: RegisterUserUseCase = Depends(RegisterUserUseCase)):
    return use_case.execute(user)


@user_router.post("/login")
async def login(user: UserLoginDTO, use_case: LoginUserUseCase = Depends(LoginUserUseCase)):
    return use_case.execute(user)
