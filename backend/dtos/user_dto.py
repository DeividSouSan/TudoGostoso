from pydantic import BaseModel
from uuid import UUID
from models.user import User


class UserDTO(BaseModel):
    id_user: UUID
    fullname: str
    username: str
    email: str

    def __init__(self, user: User):
        super().__init__(
            id_user=user.id_user,
            fullname=user.fullname,
            username=user.username,
            email=user.email
        )
