from abc import ABC, abstractmethod
from uuid import UUID
from ..models.users import User

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...
    
    @abstractmethod
    def delete(self, user: User) -> None: ...

    @abstractmethod
    def all(self) -> list[User]: ...
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> User | None: ...
    
    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def search(self, username: str) -> list[User]: ...

    @abstractmethod
    def get_by_activation_code(self, code: str) -> User | None: ...

   
