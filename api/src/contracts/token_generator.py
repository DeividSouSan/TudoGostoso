from abc import ABC, abstractmethod

class ITokenGenerator(ABC):
    @abstractmethod
    def generate(self, data: dict[str, str]): ...

    @abstractmethod
    def verify(self, token: str) -> dict[str, str]: ...