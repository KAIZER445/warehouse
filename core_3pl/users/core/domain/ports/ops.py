from abc import ABC, abstractmethod

from users.core.domain.entities.ops import Ops


class OpsPort(ABC):
    @abstractmethod
    def create(self, user_id, full_name, department=None) -> Ops: ...

    @abstractmethod
    def list_all(self) -> list[Ops]: ...
