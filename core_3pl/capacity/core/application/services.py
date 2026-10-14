from capacity.core.domain import CapacityPort, CapacityServicePort
from capacity.core.domain.entities import Capacity as CapacityEntity

class CapacityService(CapacityServicePort):
    def __init__(self, repo: CapacityPort):
        self.repo = repo

    def update_total_capacity(self, amount):
        capacity: CapacityEntity = self.repo.get()
        capacity.update_total_capacity(amount)
        self.repo.save(capacity)

    def get_capacity(self):
        return self.repo.get()

    def update_allocated_space(self, amount, operation):
        capacity: CapacityEntity = self.repo.get()
        capacity.update_allocated_space(amount, operation)
        self.repo.save(capacity)