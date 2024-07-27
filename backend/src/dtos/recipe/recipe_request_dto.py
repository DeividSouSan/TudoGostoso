from datetime import date
from typing import NewType, Union
from uuid import UUID

from pydantic import BaseModel

type Date = date


class RecipeRequestDTO(BaseModel):
    title: str
    description: Union[str, None] = None
