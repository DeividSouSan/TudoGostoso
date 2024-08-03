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
        title: str = "",
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: GetRecipesUseCase = Depends(GetRecipesUseCase),
) -> dict:

    recipes = use_case.execute(title)

    if recipes:
        recipes = [RecipeResponseDTO(user) for user in recipes]

    return {
        "recipes": recipes
    }


@recipes_router.post("")
async def create(
        recipe: RecipeCreateRequestDTO,
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: CreateRecipeUseCase = Depends(CreateRecipeUseCase),
) -> dict:
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to create a recipe."},
        )

    use_case.execute(recipe, current_user["id"])

    return {
        "message": "Recipe created successfully"
    }


@recipes_router.delete("")
async def delete(
        recipe_id: UUID | str,
        current_user: dict[str, str] = Depends(get_authorization_token),
        use_case: DeleteRecipeUseCase = Depends(DeleteRecipeUseCase)
) -> dict:

    if isinstance(recipe_id, str):
        recipe_id = UUID(recipe_id)

    use_case.execute(current_user, recipe_id)

    return {
        "message": "Recipe deleted successfully"
    }
