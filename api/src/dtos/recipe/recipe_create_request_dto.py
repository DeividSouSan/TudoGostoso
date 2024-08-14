from typing import Union

from pydantic import BaseModel


class RecipeCreateRequestDTO(BaseModel):
    title: str
    description: Union[str, None] = None
