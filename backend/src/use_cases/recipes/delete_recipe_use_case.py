from uuid import UUID

from fastapi import Depends, HTTPException, status

from ...repositories.recipe_repository import RecipeRepository


class DeleteRecipeUseCase:
    def __init__(self,
                 repository: RecipeRepository = Depends(RecipeRepository),
                 ) -> None:
        self._repository = repository

    def execute(
            self,
            token: dict[str, str],
            recipe_id: UUID = None,
            recipe_title: str = None
    ) -> None:
        if recipe_id is not None:
            recipe = self._repository.get_by_id(recipe_id)
        elif recipe_title is not None:
            recipe = self._repository.get_by_title(recipe_title)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )

        RECIPE_AUTHOR = recipe.user_id
        CURRENT_USER_ID = token["user_id"]

        if RECIPE_AUTHOR != CURRENT_USER_ID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to delete this recipe."
            )

        self._repository.delete(recipe)
