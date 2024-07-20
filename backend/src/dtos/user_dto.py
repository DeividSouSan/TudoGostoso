from typing_extensions import Annotated
from uuid import UUID

from pydantic import BaseModel, UUID4, EmailStr, Field, field_validator
from ..models.user import User


class UserDTO(BaseModel):
    id_user: UUID4
    fullname: Annotated[str, Field(min_length=3, max_length=50)]
    username: Annotated[str, Field(max_length=32)]
    email: Annotated[EmailStr, Field(max_length=64)]
    
    @field_validator('fullname', mode="before")
    @classmethod
    def fullname_must_contain_space(cls, fullname: str) -> str:
        if ' ' not in fullname:
            raise ValueError('Fullname must contain at least one (1) space.')
        return fullname.title()

    def __init__(self, user: User):
        super().__init__(
            id_user=user.id_user,
            fullname=user.fullname,
            username=user.username,
            email=user.email,
        )
