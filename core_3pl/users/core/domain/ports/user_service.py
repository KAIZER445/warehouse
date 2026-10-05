from abc import ABC, abstractmethod

from users.core.domain.entities.user import User


class UserServicePort(ABC):
    @abstractmethod
    def register(self, email, password, role, profile_data) -> User: ...

    @abstractmethod
    def list_all(self) -> list[User]: ...
