from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.src.utils.exceptions import UnauthorizedAccountDelete

from ..dtos.user.user_response_dto import UserResponseDTO
from ..routers.auth_router import oauth2_scheme
from ..use_cases.users.delete_user import DeleteUser
from ..use_cases.users.get_all_users import GetAllUsers
from ..use_cases.users.get_user import GetUser
from ..use_cases.users.search_user import SearchUser

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "",
    summary="Get all active users",
    description="Get all users that have an active account.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponseDTO],
    responses={
        status.HTTP_200_OK: {"description": "Return a list of all active users."},
    },
)
async def get_all(
    use_case: GetAllUsers = Depends(GetAllUsers),
) -> dict:

    users = use_case.execute()

    return {"users": users}


@users_router.get(
    "/{id_user:uuid}",
    summary="Get user by id",
    description="Get a user by its unique UUID id.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Return the user that matches the id."},
    },
)
async def get(
    id_user: UUID,
    use_case: GetUser = Depends(GetUser),
) -> dict:

    user = use_case.execute(id_user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"users": user}


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
    use_case: SearchUser = Depends(SearchUser),
) -> dict:

    users = use_case.execute(username)

    if users:
        users = [UserResponseDTO(user) for user in users]

    return {"users": users}


@users_router.delete(
    "/{id_user:uuid}",
    summary="Delete a user from the database",
    description="Delete a user by it's id.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "User account deleted."},
        status.HTTP_403_FORBIDDEN: {"description": "Unauthorized to delete account."},
    },
)
async def delete(
    id_user: UUID,
    current_user_token: dict[str, str] = Depends(oauth2_scheme),
    use_case: DeleteUser = Depends(DeleteUser),
) -> dict:
    try:
        use_case.execute(id_user, current_user_token)

        return {"message": "User deleted"}

    except UnauthorizedAccountDelete as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to delete account",
        )
