from abc import ABC, abstractmethod

from capacity.core.domain.entities import Capacity

class Capacity(ABC):

    @abstractmethod
    def get(self) -> Capacity: ...

    @abstractmethod
    def save(self): ...