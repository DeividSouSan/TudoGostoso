import bcrypt

from ..contracts.password_hasher import IPasswordHasher


class PasswordHasher(IPasswordHasher):
    @staticmethod
    def hash(password_text: str) -> str:
        password_text = bytes(password_text, "utf-8")
        return str(bcrypt.hashpw(password_text, bcrypt.gensalt()))

    @staticmethod
    def verify(password_text: str, password_hash: str) -> bool:
        password_text = bytes(password_text, "utf-8")
        password_hash = bytes(password_hash, "utf-8")

        return bcrypt.checkpw(password_text, password_hash)
