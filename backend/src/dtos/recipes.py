from datetime import date
from typing import Union

from pydantic import BaseModel


class Recipe(BaseModel):
    title: str
    description: Union[str, None] = None
    creation_date: date
    creator_id: str
