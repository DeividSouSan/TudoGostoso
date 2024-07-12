from typing import Union

from pydantic import BaseModel


class UserRegisterDTO(BaseModel):
    fullname: str
    email: str
    username: str
    password: str
