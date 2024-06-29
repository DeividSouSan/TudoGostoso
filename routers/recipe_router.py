from fastapi import APIRouter
from schemas.recipes import Recipe

recipe_router = APIRouter(prefix="/recipes", tags=["recipes"])


@recipe_router.get("/get-recipes")
async def get_recipes():
    return {"response": "all recipes"}


@recipe_router.post("/add-recipe")
async def add_recipe(recipe: Recipe):
    return recipe


@recipe_router.put("/update-recipe/{recipe_id}")
async def update_recipe(recipe_id: int):
    return {"response": f"updated recipe {recipe_id}"}


@recipe_router.delete("/delete-recipe/{recipe_id}")
async def delete_recipe(recipe_id: int):
    return {"response": f"deleted recipe {recipe_id}"}
