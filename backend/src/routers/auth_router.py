from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ..dtos.user.user_login_request_dto import UserLoginRequestDTO
from ..dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ..use_cases.auth.activate_account_use_case import ActivateAccountUseCase
from ..use_cases.users.login_user_use_case import LoginUserUseCase
from ..use_cases.users.register_user_use_case import RegisterUserUseCase

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register(
        user: UserRegisterRequestDTO,
        use_case: RegisterUserUseCase = Depends(RegisterUserUseCase),
) -> JSONResponse:
    """
    Registers a new user account into the database.

    Note: the account is not activated until the user verifies the activation code sent to their email.
    """
    try:
        use_case.execute(user)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User account created. Access email to activate."},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@auth_router.post("/register/verify/{activation_code:str}")
async def activate_account(
        activation_code: str,
        use_case: ActivateAccountUseCase = Depends(ActivateAccountUseCase),
) -> JSONResponse:
    """
    Activates a user account by verifying the activation code sent to the user's email.
    """
    use_case.execute(activation_code)

    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "User account activated."}
    )


@auth_router.post("/login")
async def login(
        user: UserLoginRequestDTO, use_case: LoginUserUseCase = Depends(LoginUserUseCase)
) -> JSONResponse:
    """
    Logs in a user and returns an authorization token.
    """
    try:
        token = use_case.execute(user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User authorized.", "token": token},
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
