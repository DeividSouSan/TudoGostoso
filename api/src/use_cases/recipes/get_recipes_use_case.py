from fastapi import Depends

from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class GetRecipesUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, title: str) -> list[Recipe | None]:
        if title:
            return self._repository.get_by_title(title)

        return self._repository.get()
