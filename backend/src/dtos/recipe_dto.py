from datetime import date
from typing import NewType, Union
from uuid import UUID

from pydantic import BaseModel

type Date = date

class RecipeDTO(BaseModel):
    id_recipe: UUID
    title: str
    description: Union[str, None] = None
    creation_date: Date
    creator_id: str
