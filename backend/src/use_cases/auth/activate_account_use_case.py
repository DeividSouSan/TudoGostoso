from fastapi import Depends

from ...repositories.user_repository import UserRepository


class ActivateAccountUseCase:
    def __init__(self, respository: UserRepository = Depends(UserRepository)):
        self.__repository = respository

    def execute(self, code: str):
        user = self.__repository.get_by_activation_code(code)

        if user is None:
            raise Exception("Invalid activation code.")

        # Acho que eu deveria tornar esse código uma função do repo
        user.active = True
        user.activation_code = None
        self.__repository.commit()
        print("User account activated.")
