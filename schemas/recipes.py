from pydantic import BaseModel
from typing import Union

class Recipe(BaseModel):
    name: str
    description: Union[str, None] = None
    author_id: str
