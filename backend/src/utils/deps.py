from typing import Generator

from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from ..db.connection import engine
from ..utils.token_generator import TokenGenerator


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_authorization_token(
    token: str = Header(...), token_generator: TokenGenerator = Depends(TokenGenerator)
) -> dict[str, str]:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required."
        )

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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e))
