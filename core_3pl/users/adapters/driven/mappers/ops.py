from users.core.domain.entities.ops import Ops


def to_entity(row):
    return Ops(
        id=row.id,
        user_id=row.user_id,
        full_name=row.full_name,
        department=row.department,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
