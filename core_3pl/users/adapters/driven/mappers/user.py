from users.core.domain.entities.user import User


def to_entity(row):
    return User(
        id=row.id,
        email=row.email,
        role=row.role,
        is_active=row.is_active,
        last_login=row.last_login,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
