import bcrypt


class PasswordHasher:
    @staticmethod
    def hash(password_text: str) -> bytes:
        password_text = bytes(password_text, "utf-8")
        return bcrypt.hashpw(password_text, bcrypt.gensalt())

    @staticmethod
    def verify(password_text, password_hash) -> bool:
        password_text = bytes(password_text, "utf-8")
        password_hash = bytes(password_hash, "utf-8")
        
        return bcrypt.checkpw(password_text, password_hash)
