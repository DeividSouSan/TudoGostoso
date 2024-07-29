from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.user.user_login_request_dto import UserLoginRequestDTO
from ..dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ..dtos.user.user_response_dto import UserResponseDTO
from ..use_cases.users.get_user_use_case import GetUserUseCase
from ..use_cases.users.get_users_use_case import GetUsersUseCase
from ..use_cases.users.login_user_use_case import LoginUserUseCase
from ..use_cases.users.register_user_use_case import RegisterUserUseCase

users_router = APIRouter(prefix="/users", tags=["user"])


@users_router.get("")
async def get_all(use_case: GetUsersUseCase = Depends(GetUsersUseCase)) -> JSONResponse:
    users = use_case.execute()

    users = jsonable_encoder([UserResponseDTO(user) for user in users])

    return JSONResponse(status_code=status.HTTP_200_OK, content={"users": users})


@users_router.get("/{id_user:uuid}")
async def get(id_user: UUID, use_case: GetUserUseCase = Depends(GetUserUseCase)) -> JSONResponse:
    try:
        user = use_case.execute(id_user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"users": jsonable_encoder(user)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e)}
        )


@users_router.post("")
async def register(
        user: UserRegisterRequestDTO,
        use_case: RegisterUserUseCase = Depends(RegisterUserUseCase)
) -> JSONResponse:
    try:
        use_case.execute(user)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"message": "User account created. Access email to activate."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@users_router.post("register/verify/{activatin_token}")
async def activate_account(
        activation_token: str):
    pass


@users_router.post("/login")
async def login(
        user: UserLoginRequestDTO, use_case: LoginUserUseCase = Depends(LoginUserUseCase)
) -> JSONResponse:
    try:
        token = use_case.execute(user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User authorized.", "token": token},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
