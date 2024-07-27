from datetime import datetime
from uuid import UUID

from fastapi import Depends
from ...dtos.recipe_create_dto import RecipeCreateDTO
from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class CreateRecipeUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, recipe: RecipeRequestDTO, user_id: str):

        new_recipe = Recipe(
            title=recipe.title,
            description=recipe.description,
            creation_date=datetime.now(),
            user_id=UUID(user_id),
        )

        print(new_recipe)
        self._repository.add(new_recipe)

        return new_recipe
