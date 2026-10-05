from abc import ABC, abstractmethod

from users.core.domain.entities.user import User


class UserPort(ABC):
    @abstractmethod
    def create(self, email, password, role) -> User: ...

    @abstractmethod
    def list_all(self) -> list[User]: ...
