from abc import ABC, abstractmethod

class CapacityServicePort(ABC):
    @abstractmethod
    def update_total_capacity(self, amount: int): ...

    @abstractmethod
    def get_capacity(self): ...