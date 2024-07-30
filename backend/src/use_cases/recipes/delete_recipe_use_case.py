from uuid import UUID

from fastapi import Depends, HTTPException

from ...repositories.recipe_repository import RecipeRepository


class DeleteRecipeUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(
            self,
            recipe_id: UUID = None,
            recipe_title: str = None
    ) -> None:
        if recipe_id is not None:
            recipe = self._repository.get_by_id(recipe_id)
        elif recipe_title is not None:
            recipe = self._repository.get_by_title(recipe_title)
        else:
            raise HTTPException(
                status_code=404,
                detail="Recipe not found"
            )

        self._repository.delete(recipe)
