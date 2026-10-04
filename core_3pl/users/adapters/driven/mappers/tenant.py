from users.core.domain.entities.tenant import Tenant


def to_entity(row):
    return Tenant(
        id=row.id,
        user_id=row.user_id,
        company_name=row.company_name,
        is_active=row.user.is_active,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
