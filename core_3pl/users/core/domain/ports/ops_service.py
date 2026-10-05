from abc import ABC, abstractmethod

from users.core.domain.entities.ops import Ops


class OpsServicePort(ABC):
    @abstractmethod
    def list_all(self) -> list[Ops]: ...
