from uuid import UUID

from fastapi import Depends

from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository
from ...utils.exceptions import RecipeNotFound


class GetRecipe:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, id_recipe: UUID | str) -> Recipe:
        if isinstance(id_recipe, str):
            id_recipe = UUID(id_recipe)

        recipe = self._repository.get_by_id(id_recipe)

        if not recipe:
            raise RecipeNotFound

        return recipe
