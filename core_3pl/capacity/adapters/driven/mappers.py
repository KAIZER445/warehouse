from capacity.core.domain.entities import Capacity

def to_entity(row):
    return Capacity(
        id = id,
        updated_at = row.updated_at,
        total_capacity = row.total_capacity,
        current_allocated_space = row.current_allocated_space
    )
