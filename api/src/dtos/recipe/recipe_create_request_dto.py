from datetime import date
from typing import Union

from pydantic import BaseModel

type Date = date


class RecipeCreateRequestDTO(BaseModel):
    title: str
    description: Union[str, None] = None
