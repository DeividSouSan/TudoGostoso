from datetime import datetime
from uuid import UUID

from fastapi import Depends

from ...dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class CreateRecipeUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, recipe: RecipeCreateRequestDTO, user_id: str) -> None:

        new_recipe = Recipe(
            title=recipe.title,
            description=recipe.description,
            creation_date=datetime.now(),
            user_id=UUID(user_id),
        )

        self._repository.add(new_recipe)

