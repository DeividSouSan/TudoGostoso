from uuid import UUID

from fastapi import Depends

from ...repositories.recipe_repository import RecipeRepository
from ...utils.exceptions import *


class DeleteRecipeUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)) -> None:
        self._repository = repository

    def execute(
            self,
            token: dict[str, str],
            recipe_id: UUID | None = None,
            recipe_title: str | None = None
    ) -> None:
        if recipe_id:
            recipe = self._repository.get_by_id(recipe_id)
        elif recipe_title:
            recipe = self._repository.get_by_title(recipe_title)
        else:
            raise BlankRecipeIdAndTitle()

        if not recipe:
            raise RecipeNotFound()

        RECIPE_AUTHOR = recipe.user_id
        CURRENT_USER_ID = UUID(token["id_user"])

        print(RECIPE_AUTHOR, CURRENT_USER_ID)

        if RECIPE_AUTHOR != CURRENT_USER_ID:
            raise UnauthorizedRecipeDelete()

        self._repository.delete(recipe)
