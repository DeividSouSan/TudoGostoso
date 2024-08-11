from typing import Generator

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from api.src.dtos.user.user_login_request_dto import UserLoginRequestDTO

from ..db.connection import engine
from ..utils.token_generator import TokenGenerator


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
