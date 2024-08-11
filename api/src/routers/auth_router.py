from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..contracts.email_sender import IEmailSender
from ..contracts.password_hasher import IPasswordHasher
from ..contracts.token_generator import ITokenGenerator
from ..contracts.user_repository import IUserRepository
from ..dtos.user.user_login_request_dto import UserLoginRequestDTO
from ..dtos.user.user_register_request_dto import UserRegisterRequestDTO
from ..repositories.user_repository import UserRepository
from ..use_cases.auth.activate_account import ActivateAccount
from ..use_cases.auth.login_user import LoginUser
from ..use_cases.auth.register_user import RegisterUser
from ..utils.email_sender import EmailSender
from ..utils.exceptions import *
from ..utils.password_hasher import PasswordHasher
from ..utils.token_generator import TokenGenerator

token = OAuth2PasswordBearer(tokenUrl="/auth/login")


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register",
    summary="Registers a new user account.",
    description="Registers a new deactivated user account into the database.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User account created. Access email to activate."
        },
        status.HTTP_400_BAD_REQUEST: {"description": "User account already exists."},
    },
)
async def register(
    user: UserRegisterRequestDTO,
    repository: IUserRepository = Depends(UserRepository),
    password_hasher: IPasswordHasher = Depends(PasswordHasher),
    email_sender: IEmailSender = Depends(EmailSender),
) -> dict:

    use_case = RegisterUser(repository, password_hasher, email_sender)

    try:
        use_case.execute(user)

        return {"message": "User account created. Access email to activate."}
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="User account already exists.")


@auth_router.post(
    "/register/{activation_code:str}",
    summary="Activates a new user account.",
    description="Activates a new user account by verifying the activation code sent to the user's email.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "User account activated."},
        status.HTTP_400_BAD_REQUEST: {"description": "User account already exists."},
    },
)
async def activate_account(
    activation_code: str,
    repository: IUserRepository = Depends(UserRepository),
) -> dict:
    use_case = ActivateAccount(repository)

    try:
        use_case.execute(activation_code)

        return {"message": "User account activated."}
    except AccountAlreadyActive:
        raise HTTPException(status_code=400, detail="Account already active.")


@auth_router.post(
    "/login",
    summary="Authenticate a user.",
    description="Authenticate a user by providing their email and password.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "User authorized."},
        status.HTTP_403_FORBIDDEN: {"description": "Credentials are invalid."},
    },
)
async def login(
    user: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    repository: IUserRepository = Depends(UserRepository),
    token_handler: ITokenGenerator = Depends(TokenGenerator),
    password_hasher: IPasswordHasher = Depends(PasswordHasher),
) -> dict:
    use_case = LoginUser(repository, token_handler, password_hasher)

    try:
        user = UserLoginRequestDTO(email=user.username, password=user.password)
        token = use_case.execute(user)

        return {"message": "User authorized.", "token": token}
    except UserNotFound:
        raise HTTPException(status_code=403, detail="Email not found.")
    except WrongPassword:
        raise HTTPException(status_code=403, detail="Password is incorrect.")
