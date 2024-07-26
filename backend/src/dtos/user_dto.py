from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
from typing_extensions import Annotated

from ..models.users import User
from ..dtos.recipe_dto import RecipeDTO

class UserDTO(BaseModel):
    id_user: UUID4
    fullname: Annotated[str, Field(min_length=3, max_length=50)]
    username: Annotated[str, Field(max_length=32)]
    email: Annotated[EmailStr, Field(max_length=64)]
    role: str
    recipes: list[RecipeDTO]


    @field_validator("fullname", mode="before")
    @classmethod
    def fullname_must_contain_space(cls, fullname: str) -> str:
        if " " not in fullname:
            raise ValueError("Fullname must contain at least one (1) space.")
        return fullname.title()

    def __init__(self, user: User):
        super().__init__(
            id_user=user.id_user,
            fullname=user.fullname,
            username=user.username,
            email=user.email,
            role=user.role,
            recipes=[RecipeDTO(recipe) for recipe in user.recipes]
        )
