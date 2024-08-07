from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ..dtos.recipe.recipe_response_dto import RecipeResponseDTO
from ..use_cases.recipes.create_recipe import CreateRecipe
from ..use_cases.recipes.delete_recipe import DeleteRecipe
from ..use_cases.recipes.get_all_recipes import GetAllRecipes
from ..use_cases.recipes.get_recipe import GetRecipe
from ..use_cases.recipes.search_recipe import SearchRecipe
from ..utils.exceptions import *
from ..routers.auth_router import oauth2_scheme


recipes_router = APIRouter(prefix="/recipes", tags=["Recipes"])


@recipes_router.get(
    "",
    summary="List all recipes",
    description="List all recipes in the database.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "All recipes listed successfully."

        }
    }
)
async def get_all(
    use_case: GetAllRecipes = Depends(GetAllRecipes),
    token = Depends(oauth2_scheme)
) -> dict:
    recipes = use_case.execute()

    recipes = [RecipeResponseDTO(user) for user in recipes]

    return {
        "recipes": recipes
    }


@recipes_router.get(
    "/{recipe_id:uuid}",
    summary="List a specific recipe by ID.",
    description="List a specific recipe in the database by ID.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Recipe found."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Recipe not found."
        }
    }
)
async def get(
    recipe_id: UUID,
    use_case: GetRecipe = Depends(GetRecipe),
    token = Depends(oauth2_scheme)
) -> dict:
    try:
        recipe = use_case.execute(recipe_id)

        recipe = RecipeResponseDTO(recipe)

        return {
            "recipe": recipe
        }
    except RecipeNotFound as e:
        raise HTTPException(status_code=404, detail="Recipe not found.")


@recipes_router.get(
    "search",
    summary="Search for a recipe.",
    description="Search for a recipe by it's title.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Search successful."
        }
    }
)
async def search(
    title: str,
    use_case: SearchRecipe = Depends(SearchRecipe),
    token = Depends(oauth2_scheme)
) -> dict:

    recipes = use_case.execute(title)

    if recipes:
        recipes = [RecipeResponseDTO(user) for user in recipes]

    return {
        "recipes": recipes
    }


@recipes_router.post(
    "",
    summary="Create a new recipe",
    description="Create a new recipe in the database.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Recipe created successfully."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You are not authorized to create a recipe."
        }
    }
)
async def create(
    title = Form(...),
    description = Form(...),
    use_case: CreateRecipe = Depends(CreateRecipe),
    token = Depends(oauth2_scheme)
) -> dict:
    if token["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "You are not authorized to create a recipe."},
        )

    recipe = RecipeCreateRequestDTO(title, description)

    use_case.execute(recipe, token["id"])

    return {
        "message": "Recipe created successfully"
    }


@recipes_router.delete(
    "/{recipe_id:uuid}",
    summary="Delete a recipe",
    description="Create a new recipe in the database.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Recipe created successfully."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You are not authorized to delete this recipe."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Recipe not found."
        }
    }
)
async def delete(
    recipe_id: UUID,
    use_case: DeleteRecipe = Depends(DeleteRecipe),
    token = Depends(oauth2_scheme)
) -> dict:
    try:
        use_case.execute(token, recipe_id)

        return {
            "message": "Recipe deleted successfully."
        }
    except RecipeNotFound as e:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    except UnauthorizedRecipeDelete as e:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this recipe.")
