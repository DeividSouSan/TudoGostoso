class UserAlreadyExists(Exception):
    def __init__(self, message="User already exists"):
        super().__init__(message)


class BlankRecipeIdAndTitle(Exception):
    def __init__(self, message="Must provide a recipe id or title"):
        super().__init__(message)


class RecipeNotFound(Exception):
    def __init__(self, message="Recipe not found"):
        super().__init__(message)


class UnauthorizedRecipeDelete(Exception):
    def __init__(self, message="You are not authorized to delete this recipe"):
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self, message="User not found"):
        super().__init__(message)


class WrongPassword(Exception):
    def __init__(self, message="Wrong password"):
        super().__init__(message)


class AccountAlreadyActive(Exception):
    def __init__(self, message="Account already active"):
        super().__init__(message)


class UnauthorizedAccountDelete(Exception):
    def __init__(self, message="Account already active"):
        super().__init__(message)
