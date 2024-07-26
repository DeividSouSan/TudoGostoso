from fastapi import APIRouter, Depends

from ..dtos.recipe_dto import RecipeDTO
from ..dtos.recipe_create_dto import RecipeCreateDTO
from ..utils.deps import get_authorization_token
from ..use_cases.recipes.create_recipe_use_case import CreateRecipeUseCase

recipes = APIRouter(prefix="/recipes", tags=["recipes"])


@recipes.get("")
async def get_all(token: dict[str, str] = Depends(get_authorization_token)):
    if token["role"] != "user":
        return {"message": "You are not authorized to access this resource."}

    return {"message": "Here are all the recipes"}


@recipes.post("")
async def create_recipe(
        recipe: RecipeCreateDTO,
        token: dict[str, str] = Depends(get_authorization_token),
        use_case: CreateRecipeUseCase = Depends(CreateRecipeUseCase)
    ):
    if token["role"] not in ["user", "admin"]:
        return {"message": "You are not authorized to access this resource."}

    use_case.execute(recipe, token["id_user"])

    return {"message": "Recipe created successfully"}