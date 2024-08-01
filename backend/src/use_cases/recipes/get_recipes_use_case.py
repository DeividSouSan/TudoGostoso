from uuid import UUID

from fastapi import Depends

from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class GetRecipesUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, filters: dict[str, UUID | str | None]) -> Recipe | list[Recipe | None]:
        if recipe_id := filters["id"]:
            return self._repository.get_by_id(recipe_id)

        elif title := filters["title"]:
            return self._repository.get_by_title(title)

        elif user_id := filters["user_id"]:
            return self._repository.get_by_user_id(user_id)

        return self._repository.get_all()
