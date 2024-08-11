from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password_text: str) -> str: ...

    @abstractmethod
    def verify(self, password_text: str, password_hash: str) -> bool: ...
