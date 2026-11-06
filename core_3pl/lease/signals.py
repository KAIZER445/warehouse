from django.dispatch import Signal, receiver
from lease.core.domain.entity import Lease
from inventory.models import Inventory as InventoryModel

lease_activated = Signal()


@receiver(lease_activated)
def send_books_to_storefront(sender, lease: Lease, **kwargs):
    lease_id = lease.id
    rows = InventoryModel.objects.filter(lease_id=lease_id)
    books = []
    for row in rows:
        books.append(
            {
                "id": str(row.id),
                "lease_id": str(lease_id),
                "title": row.title,
                "author": row.author,
                "description": row.description,
                "format_type": row.format_type,
                "length": str(row.length),
                "width": str(row.width),
                "thickness": str(row.thickness),
                "unit_weight": str(row.unit_weight),
                "quantity": row.quantity,
                "unit_volume": str(row.unit_volume),
                "total_volume": str(row.total_volume),
                "total_weight": str(row.total_weight),
                "created_at": row.created_at.isoformat(),
                "updated_at": row.updated_at.isoformat(),
            }
        )

    payload = {"event": "lease.activated", "lease_id": str(lease_id), "books": books}

    print(payload)
