import bcrypt

class PasswordHasher:
    def hash(self, req_password: str) -> bytes:
        return bcrypt.hashpw(req_password.encode('utf8', bcrypt.gensalt()))
        
    def verify(self, db_pwd_hash, req_password) -> bool:
        hashed = self.hash(req_password)
        
        return db_pwd_hash == hashed