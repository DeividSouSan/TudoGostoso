from typing import Union

from pydantic import BaseModel


class RegisterUserDTO(BaseModel):
    fullname: str
    email: str
    username: str
    password_1: str
    password_2: str
