from fastapi import Depends

from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class GetAllRecipes:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self) -> list[Recipe]:
        return self._repository.get()
