from ...contracts.recipe_repository import IRecipeRepository

from ...models.recipes import Recipe


class SearchRecipe:
    def __init__(self, repository: IRecipeRepository):
        self._repository = repository

    def execute(self, title: str) -> list[Recipe]:
        return self._repository.get_by_title(title)
