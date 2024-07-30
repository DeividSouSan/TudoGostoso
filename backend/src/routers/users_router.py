from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.user.user_response_dto import UserResponseDTO
from ..use_cases.users.get_user_use_case import GetUserUseCase
from ..use_cases.users.get_users_use_case import GetUsersUseCase

users_router = APIRouter(prefix="/users", tags=["user"])


@users_router.get("")
async def get_all(use_case: GetUsersUseCase = Depends(GetUsersUseCase)) -> JSONResponse:
    try:
        users = use_case.execute()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "users": jsonable_encoder([UserResponseDTO(user) for user in users])
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@users_router.get("/{id_user:uuid}")
async def get(
        id_user: UUID, use_case: GetUserUseCase = Depends(GetUserUseCase)
) -> JSONResponse:
    try:
        user = use_case.execute(id_user)

        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found."},
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"users": jsonable_encoder(user)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
