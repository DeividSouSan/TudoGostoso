from typing import Annotated, Optional, TypeVar
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.recipes import Recipe
from ..utils.deps import get_db
from ..utils.exceptions import UserAlreadyExistsError


class RecipeRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self.__session = session

    def add(self, recipe: Recipe) -> None:
        self.__session.add(recipe)
        self.__session.commit()