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

    def get_all(self) -> list[Recipe]:
        return self.__session.query(Recipe).all()

    def get_by_id(self, id: UUID) -> Recipe:
        return self.__session.query(Recipe).filter(Recipe.id == id).first()

    def get_by_title(self, title: str) -> Recipe:
        return self.__session.query(Recipe).filter(Recipe.title == title).first()

    def delete(self, recipe: Recipe) -> None:
        self.__session.delete(recipe)
        self.__session.commit()
