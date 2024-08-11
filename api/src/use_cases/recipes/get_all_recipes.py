from ...contracts.recipe_repository import IRecipeRepository
from ...models.recipes import Recipe


class GetAllRecipes:
    def __init__(self, repository: IRecipeRepository):
        self._repository = repository

    def execute(self) -> list[Recipe]:
        return self._repository.get()
