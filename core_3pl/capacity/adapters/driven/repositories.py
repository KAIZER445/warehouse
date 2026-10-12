from capacity.core.domain.ports import Capacity as CapacityPort
from capacity.models import Capacity as CapacityModel

from .mappers import to_entity

class CapacityRepository(CapacityPort):

    def get(self):
        return to_entity(CapacityModel.objects.first())

    def save(self, capacity):
        CapacityModel.objects.filter(id=capacity.id).update(
            total_capacity=capacity.total_capacity,
            current_allocated_space=capacity.current_allocated_space,
        )
