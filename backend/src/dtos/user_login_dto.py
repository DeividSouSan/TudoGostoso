from pydantic import BaseModel, EmailStr

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str
