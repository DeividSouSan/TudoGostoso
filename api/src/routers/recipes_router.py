from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ..dtos.recipe.recipe_response_dto import RecipeResponseDTO
from ..routers.auth_router import oauth2_scheme
from ..use_cases.recipes.create_recipe import CreateRecipe
from ..use_cases.recipes.delete_recipe import DeleteRecipe
from ..use_cases.recipes.get_all_recipes import GetAllRecipes
from ..use_cases.recipes.get_recipe import GetRecipe
from ..use_cases.recipes.search_recipe import SearchRecipe
from ..utils.exceptions import *

recipes_router = APIRouter(prefix="/recipes", tags=["Recipes"])


@recipes_router.get(
    "",
    summary="List all recipes",
    description="List all recipes in the database.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    response_model=list[RecipeResponseDTO],
    responses={status.HTTP_200_OK: {"description": "All recipes listed successfully."}},
)
async def get_all(
    use_case: GetAllRecipes = Depends(GetAllRecipes),
) -> dict:
    recipes = use_case.execute()

    return {"recipes": recipes}


@recipes_router.get(
    "/{recipe_id:uuid}",
    summary="List a specific recipe by ID.",
    description="List a specific recipe in the database by ID.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    response_model=RecipeResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Recipe found."},
        status.HTTP_404_NOT_FOUND: {"description": "Recipe not found."},
    },
)
async def get(
    recipe_id: UUID,
    use_case: GetRecipe = Depends(GetRecipe),
) -> dict:
    try:
        recipe = use_case.execute(recipe_id)

        return {"recipe": recipe}
    except RecipeNotFound:
        raise HTTPException(status_code=404, detail="Recipe not found.")


@recipes_router.get(
    "/search",
    summary="Search for a recipe.",
    description="Search for a recipe by it's title.",
    dependencies=[Depends(oauth2_scheme)],
    status_code=status.HTTP_200_OK,
    response_model=list[RecipeResponseDTO],
    responses={status.HTTP_200_OK: {"description": "Search successful."}},
)
async def search(
    title: str,
    use_case: SearchRecipe = Depends(SearchRecipe),
) -> dict:

    recipes = use_case.execute(title)

    return {"recipes": recipes}


@recipes_router.post(
    "",
    summary="Create a new recipe",
    description="Create a new recipe in the database.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Recipe created successfully."},
        status.HTTP_403_FORBIDDEN: {
            "description": "You are not authorized to create a recipe."
        },
    },
)
async def create(
    title=Form(...),
    description=Form(...),
    use_case: CreateRecipe = Depends(CreateRecipe),
    current_user_token=Depends(oauth2_scheme),
) -> dict:

    recipe = RecipeCreateRequestDTO(title, description)

    use_case.execute(recipe, current_user_token["id_user"])

    return {"message": "Recipe created successfully"}


@recipes_router.delete(
    "/{recipe_id:uuid}",
    summary="Delete a recipe",
    description="Create a new recipe in the database.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Recipe created successfully."},
        status.HTTP_403_FORBIDDEN: {
            "description": "You are not authorized to delete this recipe."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Recipe not found."},
    },
)
async def delete(
    recipe_id: UUID,
    use_case: DeleteRecipe = Depends(DeleteRecipe),
    current_user_token=Depends(oauth2_scheme),
) -> dict:
    try:
        use_case.execute(
            current_user_token["role"], current_user_token["id"], recipe_id
        )

        return {"message": "Recipe deleted successfully."}
    except RecipeNotFound:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    except UnauthorizedRecipeDelete:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this recipe."
        )
