import os
from datetime import UTC, datetime, timedelta

from jose import jwt

from ..contracts.token_generator import ITokenGenerator


class TokenGenerator(ITokenGenerator):
    def __init__(self):
        from dotenv import load_dotenv

        load_dotenv()

        self.__secret_key: str = os.getenv("SECRET_KEY")
        self.__algorithm: str = os.getenv("ALGORITHM") or "HS256"
        self.__expires: float = float(os.getenv("EXPIRATION_MINUTES"))

    def generate(self, data: dict[str, str]):
        claims = data.copy()

        expire = datetime.now(UTC) + timedelta(minutes=float(self.__expires))
        claims["exp"] = expire

        encoded_jwt = jwt.encode(
            claims=claims, key=self.__secret_key, algorithm=self.__algorithm
        )

        return encoded_jwt

    def verify(self, token: str) -> dict[str, str]:
        decoded_jwt = jwt.decode(
            token=token, key=self.__secret_key, algorithms=[self.__algorithm]
        )

        return decoded_jwt
