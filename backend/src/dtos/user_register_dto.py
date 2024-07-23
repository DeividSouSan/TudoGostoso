from typing_extensions import Annotated
from pydantic import BaseModel, field_validator, EmailStr, Field
import re

class UserRegisterDTO(BaseModel):
    fullname: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[EmailStr, Field(max_length=64)]
    username: Annotated[str, Field(max_length=32)]
    password: Annotated[str, Field(min_length=8, max_length=64)]

    @field_validator('fullname', mode="before")
    @classmethod
    def fullname_must_contain_space(cls, value: str) -> str:
        if ' ' not in value:
            raise ValueError('Fullname must contain at least one (1) space.')
        return value.title()
    
    @field_validator('password')
    @classmethod
    def password_complexity(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[a-z]', value):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula.')
        if not re.search(r'[0-9]', value):
            raise ValueError('A senha deve conter pelo menos um número.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('A senha deve conter pelo menos um caractere especial.')
        return value