from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ..dtos.recipe.recipe_response_dto import RecipeResponseDTO
from ..use_cases.recipes.create_recipe_use_case import CreateRecipeUseCase
from ..use_cases.recipes.delete_recipe_use_case import DeleteRecipeUseCase
from ..use_cases.recipes.get_recipes_use_case import GetRecipesUseCase
from ..utils.deps import get_authorization_token

recipes_router = APIRouter(prefix="/recipes", tags=["recipes"])


@recipes_router.get("")
async def get(
        title: str | None = None,
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: GetRecipesUseCase = Depends(GetRecipesUseCase),
) -> JSONResponse:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to view recipes."},
        )

    recipes = use_case.execute(title)

    if recipes:
        recipes = [RecipeResponseDTO(user) for user in recipes]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"recipes": jsonable_encoder(recipes)}
    )


@recipes_router.post("")
async def create(
        recipe: RecipeCreateRequestDTO,
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: CreateRecipeUseCase = Depends(CreateRecipeUseCase),
) -> JSONResponse:
    if token["role"] not in ["user"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to create a recipe."},
        )

    use_case.execute(recipe, token["id_user"])

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Recipe created successfully"},
    )


@recipes_router.delete("")
async def delete(
        recipe_id: UUID | None = None,
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: DeleteRecipeUseCase = Depends(DeleteRecipeUseCase)
) -> JSONResponse:
    if token["role"] not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to create a recipe."},
        )

    use_case.execute(token, recipe_id)  # talvez passar só o role já fosse suficiente

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Recipe deleted successfully."}
    )
