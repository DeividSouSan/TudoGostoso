from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from ..dtos.user_register_dto import UserRegisterDTO
from ..dtos.user_login_dto import UserLoginDTO
from ..dtos.user_dto import UserDTO
from ..use_cases.users.login_user_use_case import LoginUserUseCase
from ..use_cases.users.register_user_use_case import RegisterUserUseCase
from ..use_cases.users.get_user_use_case import GetUserUseCase
from ..use_cases.users.get_users_use_case import GetUsersUseCase
from ..models.users import User
from fastapi.encoders import jsonable_encoder

users = APIRouter(prefix="/users", tags=["user"])


@users.get("")
async def get_all(use_case: GetUsersUseCase = Depends(GetUsersUseCase)) -> JSONResponse:
    users = use_case.execute()
    
    users = list(map(UserDTO, users))
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"users": jsonable_encoder(users)}
    )

@users.get("/{id_user:uuid}")
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


@users.post("")
async def register(user: UserRegisterDTO, use_case: RegisterUserUseCase = Depends(RegisterUserUseCase)) -> JSONResponse:
    try:
        use_case.execute(user)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User created"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )

@users.post("/login")
async def login(user: UserLoginDTO, use_case: LoginUserUseCase = Depends(LoginUserUseCase)) -> JSONResponse:
    try:
        token = use_case.execute(user)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "User authorized.",
                "token": token}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )
