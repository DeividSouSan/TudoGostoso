from typing import Annotated

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
