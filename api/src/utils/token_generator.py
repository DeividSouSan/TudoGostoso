import os
from datetime import UTC, datetime, timedelta

from jose import jwt


class TokenGenerator:
    def __init__(self, expiration_minutes: int = 30):
        from dotenv import load_dotenv

        load_dotenv()

        self.__secret_key = os.getenv("SECRET_KEY")
        self.__algorithm = os.getenv("ALGORITHM") or "HS256"
        self.__expires = int(os.getenv("EXPIRATION_MINUTES")) or expiration_minutes

    def generate(self, data: dict[str, str]):
        claims = data.copy()

        expire = datetime.now(UTC) + timedelta(minutes=self.__expires)
        claims.update({"exp": expire})

        encoded_jwt = jwt.encode(
            claims=claims,
            key=self.__secret_key,
            algorithm=self.__algorithm
        )

        return encoded_jwt

    def verify(self, token: str) -> dict[str, str]:
        decoded_jwt = jwt.decode(
            token=token,
            key=self.__secret_key,
            algorithms=[self.__algorithm]
        )

        return decoded_jwt
