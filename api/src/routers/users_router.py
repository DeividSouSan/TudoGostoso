from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Security
from fastapi.responses import JSONResponse

from ..dtos.user.user_response_dto import UserResponseDTO
from ..routers.auth_router import oauth2_scheme
from ..use_cases.users.get_all_users import GetAllUsers
from ..use_cases.users.get_user import GetUser
from ..use_cases.users.search_user import SearchUser
from ..utils.deps import get_authorization_token

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get(
    "",
    summary="Get all active users",
    description="Get all users that have an active account.",
)
async def get_all(
    use_case: GetAllUsers = Depends(GetAllUsers), token=Depends(oauth2_scheme)
) -> dict:

    users = use_case.execute()

    if users:
        users = [UserResponseDTO(user) for user in users]

    return {"users": users}


@users_router.get(
    "/{id:uuid}",
    summary="Get user by id",
    description="Get a user by its unique UUID id.",
)
async def get(
    id: UUID,
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: GetUser = Depends(GetUser),
    token=Depends(oauth2_scheme),
) -> dict:

    user = use_case.execute(current_user["id"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user = UserResponseDTO(user)

    return {"users": user}


@users_router.get(
    "/search",
    summary="Search for users by parameters",
    description="Search for users by username or email.",
)
async def search(
    username: str = "",
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: SearchUser = Depends(SearchUser),
    token=Depends(oauth2_scheme),
) -> dict:

    users = use_case.execute(username)

    if users:
        users = [UserResponseDTO(user) for user in users]

    return {"users": users}


@users_router.delete("/{id:uuid}")
async def delete(
    username: str = "",
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: SearchUser = Depends(SearchUser),
    token=Depends(oauth2_scheme),
) -> dict:

    pass
