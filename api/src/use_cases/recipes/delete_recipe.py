from uuid import UUID

from fastapi import Depends

from ...repositories.recipe_repository import RecipeRepository
from ...utils.exceptions import *


class DeleteRecipe:
    def __init__(
        self, repository: RecipeRepository = Depends(RecipeRepository)
    ) -> None:
        self._repository = repository

    def execute(
        self,
        current_user: dict,
        recipe_id: UUID,
    ) -> None:
        recipe = self._repository.get_by_id(recipe_id)

        if not recipe:
            raise RecipeNotFound()

        if current_user["role"] == "user":
            RECIPE_AUTHOR = recipe.user_id
            CURRENT_USER_ID = UUID(current_user["id"])

            if RECIPE_AUTHOR != CURRENT_USER_ID:
                raise UnauthorizedRecipeDelete()

        self._repository.delete(recipe)
