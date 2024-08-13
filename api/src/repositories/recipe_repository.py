from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from ..contracts.recipe_repository import IRecipeRepository
from ..models.recipes import Recipe
from ..utils.deps import get_db


class RecipeRepository(IRecipeRepository):
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self.__session = session

    def add(self, recipe: Recipe) -> None:
        self.__session.add(recipe)
        self.__session.commit()

    def all(self) -> list[Recipe]:
        return self.__session.query(Recipe).all()

    def get_by_id(self, recipe_id: UUID) -> Recipe | None:
        return (
            self.__session.query(Recipe).filter(Recipe.id_recipe == recipe_id).first()
        )

    def get_by_title(self, title: str) -> list[Recipe]:
        return (
            self.__session.query(Recipe).filter(Recipe.title.like(f"%{title}%")).all()
        )

    def get_by_user_id(self, user_id: UUID) -> list[Recipe]:
        return self.__session.query(Recipe).filter(Recipe.user_id == user_id).all()

    def delete(self, recipe: Recipe) -> None:
        self.__session.delete(recipe)
        self.__session.commit()
