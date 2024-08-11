from abc import ABC, abstractmethod
from uuid import UUID

from ..models.recipes import Recipe


class IRecipeRepository(ABC):
    @abstractmethod
    def add(self, recipe: Recipe) -> None: ...

    @abstractmethod
    def delete(self, recipe: Recipe) -> None: ...
    
    @abstractmethod
    def all(self) -> list[Recipe]: ...

    @abstractmethod
    def get_by_id(self, recipe_id: UUID) -> Recipe | None: ...

    @abstractmethod
    def get_by_title(self, title: str) -> list[Recipe]: ...

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> list[Recipe]: ...

