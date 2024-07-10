from typing import Union

from pydantic import BaseModel


class Recipe(BaseModel):
    name: str
    description: Union[str, None] = None
    author_id: str
