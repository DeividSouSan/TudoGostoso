from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.user.user_response_dto import UserResponseDTO
from ..use_cases.users.get_users_use_case import GetUsersUseCase
from ..utils.deps import get_authorization_token

users_router = APIRouter(prefix="/users", tags=["user"])


@users_router.get("")
async def get(
        id_user: UUID | None = None,
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: GetUsersUseCase = Depends(GetUsersUseCase)
) -> JSONResponse:
    if token["role"] not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to create a recipe."},
        )

    users = use_case.execute(id_user)

    if users:
        users = [UserResponseDTO(user) for user in users]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"users": jsonable_encoder(users)}
    )
