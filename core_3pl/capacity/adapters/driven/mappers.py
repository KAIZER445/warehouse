from capacity.core.domain.entities import Capacity

def to_entity(row):
    if row is None:
        return None
    return Capacity(
        id = row.id,
        updated_at = row.updated_at,
        total_capacity = row.total_capacity,
        current_allocated_space = row.current_allocated_space
    )
