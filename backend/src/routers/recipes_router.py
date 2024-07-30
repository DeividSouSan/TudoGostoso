from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ..dtos.recipe.recipe_response_dto import RecipeResponseDTO
from ..use_cases.recipes.create_recipe_use_case import CreateRecipeUseCase
from ..use_cases.recipes.delete_recipe_use_case import DeleteRecipeUseCase
from ..use_cases.recipes.get_all_recipes_use_case import GetAllRecipesUseCase
from ..utils.deps import get_authorization_token

recipes_router = APIRouter(prefix="/recipes", tags=["recipes"])


@recipes_router.get("")
async def get_all(
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: GetAllRecipesUseCase = Depends(GetAllRecipesUseCase),
) -> JSONResponse:
    if token["role"] != "user":
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "You are not authorized to view recipes."},
        )

    try:
        recipes = use_case.execute()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "recipes": jsonable_encoder(
                    [RecipeResponseDTO(recipe) for recipe in recipes]
                )
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@recipes_router.post("")
async def create(
        recipe: RecipeCreateRequestDTO,
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: CreateRecipeUseCase = Depends(CreateRecipeUseCase),
) -> JSONResponse:
    if token["role"] not in ["user", "admin"]:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "You are not authorized to create a recipe."},
        )

    try:
        use_case.execute(recipe, token["id_user"])

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Recipe created successfully"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )


@recipes_router.delete("")
async def delete(
        recipe_id: UUID = None,
        recipe_title: str = None,
        use_case: DeleteRecipeUseCase = Depends(DeleteRecipeUseCase)
) -> JSONResponse:
    try:
        use_case.execute(recipe_id, recipe_title)

        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"message": "Recipe deleted successfully."}
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.detail}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)}
        )
