class UserAlreadyExistsError(Exception):
    def __init__(self, message="User already exists"):
        super().__init__(message)
