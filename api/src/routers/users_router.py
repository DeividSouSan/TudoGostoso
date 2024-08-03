from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..use_cases.users.search_user import SearchUser

from ..use_cases.users.get_all_users import GetAllUsers
from ..use_cases.users.get_user import GetUser

from ..dtos.user.user_response_dto import UserResponseDTO
from ..use_cases.users.get_all_users import GetAllUsers
from ..use_cases.users.get_user import GetUser
from ..utils.deps import get_authorization_token

users_router = APIRouter(prefix="/users", tags=["user"])


@users_router.get("")
async def get_all(
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: GetAllUsers = Depends(GetAllUsers)
) -> dict:

    users = use_case.execute()

    if users:
        users = [UserResponseDTO(user) for user in users]

    return {
        "users":users
    }


@users_router.get("/{id:uuid}")
async def get(
        id: UUID,
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: GetUser = Depends(GetUser)
) -> dict:

    user = use_case.execute(current_user["id"])

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = UserResponseDTO(user)

    return {
        "users": user
    }


@users_router.get("/search")
async def search(
        username: str = "",
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: SearchUser = Depends(SearchUser)
) -> dict:

    users = use_case.execute(username)

    if users:
        users = [UserResponseDTO(user) for user in users]

    return {
        "users": users
    }

@users_router.delete("/{id:uuid}")
async def delete(
        username: str = "",
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: SearchUser = Depends(SearchUser)
) -> dict:

    pass
