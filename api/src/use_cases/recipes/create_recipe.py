from datetime import datetime
from uuid import UUID

from ...contracts.recipe_repository import IRecipeRepository
from ...dtos.recipe.recipe_create_request_dto import RecipeCreateRequestDTO
from ...models.recipes import Recipe


class CreateRecipe:
    def __init__(self, repository: IRecipeRepository):
        self._repository = repository

    def execute(self, recipe: RecipeCreateRequestDTO, user_id: UUID) -> None:
        new_recipe = Recipe(
            title=recipe.title,
            description=recipe.description,
            creation_date=datetime.now(),
            user_id=user_id,
        )

        self._repository.add(new_recipe)
