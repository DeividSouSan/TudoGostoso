from datetime import datetime
from uuid import UUID

from fastapi import Depends

from src.dtos.recipe.recipe_request_dto import RecipeRequestDTO
from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class GetAllRecipesUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self) -> list[Recipe]:
        return self._repository.get_all()
