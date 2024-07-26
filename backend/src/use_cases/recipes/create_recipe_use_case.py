from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException, status

from ...dtos.recipe_dto import RecipeDTO
from ...dtos.recipe_create_dto import RecipeCreateDTO
from ...models.recipes import Recipe
from ...repositories.recipe_repository import RecipeRepository


class CreateRecipeUseCase:
    def __init__(self, repository: RecipeRepository = Depends(RecipeRepository)):
        self._repository = repository

    def execute(self, recipe: RecipeCreateDTO, user_id: UUID):
        
        new_recipe = Recipe(
            title=recipe.title,
            description=recipe.description,
            creation_date=datetime.now(),
            user_id=user_id
        )
        
        print(new_recipe)
        self._repository.add(new_recipe)

        return new_recipe
