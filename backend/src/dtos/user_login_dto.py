import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing_extensions import Annotated


class UserLoginDTO(BaseModel):
    email: Annotated[EmailStr, Field(max_length=64)]
    password: Annotated[str, Field(min_length=8, max_length=64)]

    @field_validator("password")
    @classmethod
    def password_complexity(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"[0-9]", value):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("A senha deve conter pelo menos um caractere especial.")
        return value
