from fastapi import Depends, HTTPException

from ...repositories.user_repository import UserRepository


class ActivateAccountUseCase:
    def __init__(self, respository: UserRepository = Depends(UserRepository)):
        self.__repository = respository

    def execute(self, code: str) -> None:
        user = self.__repository.get_by_activation_code(code)

        if user is None:
            raise HTTPException(
                status_code=400,
                detail="Account already activated or invalid activation code."
            )

        user.active = True
        user.activation_code = None

        self.__repository.commit()
