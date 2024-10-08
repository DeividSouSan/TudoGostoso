from datetime import date
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class RecipeResponseDTO(BaseModel):
    id_recipe: UUID
    title: str
    description: Union[str, None] = None
    creation_date: date
    creator_id: UUID

    def __init__(self, recipe):
        super().__init__(
            id_recipe=recipe.id_recipe,
            title=recipe.title,
            description=recipe.description,
            creation_date=recipe.creation_date,
            creator_id=recipe.user_id,
        )
