from abc import ABC, abstractmethod

class Capacity(ABC):
    @abstractmethod
    def update_total_capacity(self, amount: int): ...