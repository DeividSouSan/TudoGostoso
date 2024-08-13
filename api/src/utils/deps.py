from typing import Generator

from fastapi import Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from ..contracts.token_generator import ITokenGenerator


from ..db.connection import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_authorization_token(token: str, token_generator: ITokenGenerator) -> dict[str, str]:
    try:
        token_data = token_generator.verify(token)

        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature has expired.",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token is invalid"
        )
