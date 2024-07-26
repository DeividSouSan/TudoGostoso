from uuid import UUID

from fastapi import Depends, HTTPException, status

from ...dtos.recipe_dto import RecipeDTO
from ...repositories.recipe_repository import RecipeRepository


class CreateRecipeUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, recipe: RecipeDTO):
        self._repository.create(recipe)

        return recipe
