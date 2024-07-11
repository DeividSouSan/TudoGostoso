from fastapi import APIRouter
from src.dtos.recipes import Recipe

recipe_router = APIRouter(prefix="/recipes", tags=["recipes"])


@recipe_router.get("")
async def get_recipes():
    return {"response": "all recipes"}


@recipe_router.post("")
async def add_recipe(recipe: Recipe):
    return recipe


@recipe_router.put("{recipe_id}")
async def update_recipe(recipe_id: int):
    return {"response": f"updated recipe {recipe_id}"}


@recipe_router.delete("{recipe_id}")
async def delete_recipe(recipe_id: int):
    return {"response": f"deleted recipe {recipe_id}"}
