from lease.core.domain.ports import Lease as LeasePort
from lease.models import Lease as LeaseModel
from inventory.models import Inventory as InventoryModel
from lease.core.domain.book import Book
from .mappers import to_entity
from uuid import UUID
from lease.core.domain.entity import Lease
from django.db import transaction
from django.utils import timezone

class LeaseRepository(LeasePort):

    def list_by_tenant(self, tenant_id):
        rows = LeaseModel.objects.filter(tenant_id = tenant_id)
        leases = []
        for row in rows:
            leases.append(to_entity(row))
        return leases

    @transaction.atomic
    def save(self, lease: Lease, books: list[Book]) -> UUID:
        leaseRow = LeaseModel.objects.create(
            tenant_id=lease.tenant_id,
            box_combination=lease.box_combination,
            total_boxes=lease.total_boxes,
            minimum_required_space=lease.minimum_required_space,
            total_volume=lease.total_volume,
            total_weight=lease.total_weight,
            status=lease.status,
        )
        InventoryModel.objects.bulk_create(
            [
                InventoryModel(
                    lease_id=leaseRow.id,
                    title=book.title,
                    author=book.author,
                    description=book.description,
                    format_type=book.format_type,
                    length=book.length,
                    width=book.width,
                    thickness=book.thickness,
                    unit_weight=book.unit_weight,
                    quantity=book.quantity,
                    unit_volume=book.unit_volume,
                    total_volume=book.total_volume,
                    total_weight=book.total_weight,
                )
                for book in books
            ]
        )
        return leaseRow.id

    def get_by_id_and_tenant(self, lease_id, tenant_id):
        row = LeaseModel.objects.filter(id = lease_id, tenant_id = tenant_id).first()
        if row is not None:
            return to_entity(row)
        else:
            return None

    def activate(self, lease: Lease):
        row = LeaseModel.objects.get(id=lease.id)
        row.selected_space = lease.selected_space
        row.term_months = lease.term_months
        row.start_date = lease.start_date
        row.end_date = lease.end_date
        row.status = lease.status
        row.save()