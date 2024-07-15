import bcrypt


class PasswordHasher:
    @staticmethod
    def hash(self, password_text: str) -> bytes:
        return bcrypt.hashpw(password_text.encode("utf8", bcrypt.gensalt()))

    @staticmethod
    def verify(self, password_text, password_hash) -> bool:
        password_text = bytes(password_text)
        password_hash = bytes(password_hash)
        
        return bcrypt.checkpw(password_text, password_hash)
