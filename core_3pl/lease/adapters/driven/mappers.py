from lease.core.domain.entity import Lease


def to_entity(row) -> Lease:
    return Lease(
        id=row.id,
        tenant_id=row.tenant_id,
        box_combination=row.box_combination,
        total_boxes=row.total_boxes,
        minimum_required_space=row.minimum_required_space,
        total_volume=row.total_volume,
        total_weight=row.total_weight,
        status=row.status,
        selected_space=row.selected_space,
        term_months=row.term_months,
        start_date=row.start_date,
        end_date=row.end_date,
    )