from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.recipes import Recipe
from ..utils.deps import get_db


class RecipeRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self.__session = session

    def add(self, recipe: Recipe) -> None:
        self.__session.add(recipe)
        self.__session.commit()

    def get(self) -> list[Recipe]:
        query = self.__session.query(Recipe)
        return query.all()

    def get_by_id(self, recipe_id: UUID) -> Recipe | None:
        query = self.__session.query(Recipe).filter(Recipe.id_recipe == recipe_id)
        return query.first()

    def get_by_title(self, title: str) -> list[Recipe]:
        query = self.__session.query(Recipe).filter(Recipe.title.like(f"%{title}%"))
        return query.all()

    def get_by_user_id(self, user_id: UUID) -> list[Recipe]:
        query = self.__session.query(Recipe).filter(Recipe.user_id == user_id)
        return query.all()

    def delete(self, recipe: Recipe) -> None:
        self.__session.delete(recipe)
        self.__session.commit()
