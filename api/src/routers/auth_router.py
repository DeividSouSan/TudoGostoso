from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..dtos.user.user_login_request_dto import UserLoginRequestDTO
from ..dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ..use_cases.auth.activate_account import ActivateAccount
from ..use_cases.auth.login_user import LoginUser
from ..use_cases.auth.register_user import RegisterUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register",
    summary="Registers a new user account.",
    description="Registers a new deactivated user account into the database.",
)
async def register(
    user: UserRegisterRequestDTO,
    use_case: RegisterUser = Depends(RegisterUser),
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

@auth_router.post("/register/{activation_code:str}")
async def activate_account(
    activation_code: str,  # Pydantic poderia validar esse parâmetro
    use_case: ActivateAccount = Depends(ActivateAccount),
) -> JSONResponse:
    """
    Activates a user account by verifying the activation code sent to the user's email.
    """
    try:
        use_case.execute(activation_code)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User account activated."},
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})



@auth_router.post("/login")
async def login(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    use_case: LoginUser = Depends(LoginUser),
) -> JSONResponse:
    """
    Logs in a user and returns an authorization token.
    """

    try:
        user = UserLoginRequestDTO(email=user.username, password=user.password)
        token = use_case.execute(user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User authorized.", "token": token},
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})
