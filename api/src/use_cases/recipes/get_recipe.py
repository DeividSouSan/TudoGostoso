from uuid import UUID

from fastapi import Depends

from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class GetRecipe:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, id: UUID | str) -> Recipe:
        if isinstance(id, str):
            id = UUID(id)

        return self._repository.get_by_id(id)
