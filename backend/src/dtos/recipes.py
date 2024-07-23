from typing import Union

from pydantic import BaseModel
from datetime import date


class Recipe(BaseModel):
    title: str
    description: Union[str, None] = None
    creation_date: date
    creator_id: str
    
