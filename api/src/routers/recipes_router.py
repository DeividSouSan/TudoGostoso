from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ..dtos.recipe.recipe_response_dto import RecipeResponseDTO
from ..use_cases.recipes.create_recipe import CreateRecipe
from ..use_cases.recipes.delete_recipe import DeleteRecipe
from ..use_cases.recipes.get_all_recipes import GetAllRecipes
from ..use_cases.recipes.get_recipe import GetRecipe
from ..use_cases.recipes.search_recipe import SearchRecipe
from ..utils.deps import get_authorization_token
from ..routers.auth_router import oauth2_scheme


recipes_router = APIRouter(prefix="/recipes", tags=["Recipes"])


@recipes_router.get("")
async def get_all(
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: GetAllRecipes = Depends(GetAllRecipes),
    token = Depends(oauth2_scheme)
) -> dict:

    recipes = use_case.execute()

    if recipes:
        recipes = [RecipeResponseDTO(user) for user in recipes]

    return {"recipes": recipes}


@recipes_router.get("/{recipe_id:uuid}")
async def get(
    id: UUID,
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: GetRecipe = Depends(GetRecipe),
    token = Depends(oauth2_scheme)
) -> dict:

    recipe = use_case.execute(id)

    recipe = RecipeResponseDTO(recipe)

    return {"recipes": recipe}


@recipes_router.get("search")
async def search(
    title: str = "",
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: SearchRecipe = Depends(SearchRecipe),
    token = Depends(oauth2_scheme)
) -> dict:

    recipes = use_case.execute(title)

    if recipes:
        recipes = [RecipeResponseDTO(user) for user in recipes]

    return {"recipes": recipes}


@recipes_router.post("")
async def create(
    recipe: RecipeCreateRequestDTO,
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: CreateRecipe = Depends(CreateRecipe),
    token = Depends(oauth2_scheme)
) -> dict:
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to create a recipe."},
        )

    use_case.execute(recipe, current_user["id"])

    return {"message": "Recipe created successfully"}


@recipes_router.delete("")
async def delete(
    recipe_id: UUID | str,
    current_user: dict[str, str] = Depends(get_authorization_token),
    use_case: DeleteRecipe = Depends(DeleteRecipe),
    token = Depends(oauth2_scheme)
) -> dict:

    if isinstance(recipe_id, str):
        recipe_id = UUID(recipe_id)

    use_case.execute(current_user, recipe_id)

    return {"message": "Recipe deleted successfully"}
