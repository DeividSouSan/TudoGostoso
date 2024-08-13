from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..utils.token_generator import TokenGenerator

from ..contracts.user_repository import IUserRepository
from ..repositories.user_repository import UserRepository

from ..utils.exceptions import UnauthorizedAccountDelete

from ..dtos.user.user_response_dto import UserResponseDTO
from ..routers.auth_router import oauth2_scheme
from ..use_cases.users.delete_user import DeleteUser
from ..use_cases.users.get_all_users import GetAllUsers
from ..use_cases.users.get_user import GetUser
from ..use_cases.users.search_user import SearchUser
from ..utils.deps import get_authorization_token

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "",
    summary="Get all active users",
    description="Get all users that have an active account.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Return a list of all active users."},
    },
)
async def get_all(
    repository: IUserRepository = Depends(UserRepository),
) -> dict:

    use_case = GetAllUsers(repository)
    users = use_case.execute()
    
    if users:
        users = [UserResponseDTO(user) for user in users]


    return {"users": users}


@users_router.get(
    "/{id_user:uuid}",
    summary="Get user by id",
    description="Get a user by its unique UUID id.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Return the user that matches the id."},
    },
)
async def get(
    id_user: UUID,
    repository: IUserRepository = Depends(UserRepository)
) -> dict:
    use_case = GetUser(repository)
    user = use_case.execute(id_user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"users": UserResponseDTO(user)}


@users_router.get(
    "/search",
    summary="Search for users by parameters",
    description="Search for users by username or email.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    response_model=dict[str, list[UserResponseDTO]],
    responses={
        status.HTTP_200_OK: {
            "description": "Return a list of users that match the search criteria."
        },
    },
)
async def search(
    username: str,
    repository: IUserRepository = Depends(UserRepository)
) -> dict:
    use_case = SearchUser(repository)
    users = use_case.execute(username)

    if users:
        users = [UserResponseDTO(user) for user in users]

    return {"users": users}


@users_router.delete(
    "/{id_user:uuid}",
    summary="Delete a user from the database",
    description="Delete a user by it's id.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "User account deleted."},
        status.HTTP_403_FORBIDDEN: {"description": "Unauthorized to delete account."},
    },
)
async def delete(
    id_user: UUID,
    repository: IUserRepository = Depends(UserRepository),
    token: str = Depends(oauth2_scheme),
    token_generator = Depends(TokenGenerator)
) -> dict:
    current_user = get_authorization_token(token, token_generator)
    use_case = DeleteUser(repository)
    
    try:
        use_case.execute(id_user, current_user)

        return {"message": "User deleted"}

    except UnauthorizedAccountDelete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to delete account",
        )
