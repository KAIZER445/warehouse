from lease.core.domain.ports_service import LeaseServicePort
from lease.core.domain.ports import Lease as LeasePort
from lease.core.domain.entity import Lease
from lease.core.domain.dto import QuoteResult
from django.db import transaction

class LeaseService(LeaseServicePort):
    def __init__(self, repo: LeasePort):
        self.repo = repo

    def create_quote(self, tenant_id, books):
        lease = Lease.create_quote(tenant_id=tenant_id, books = books)
        lease_id = self.repo.save(lease=lease, books=books)
        return QuoteResult(
            lease_id = lease_id,
            status=lease.status,
            minimum_required_space = lease.minimum_required_space,
            box_combination = lease.box_combination
        )

    @transaction.atomic
    def activate_lease(self, lease_id, tenant_id, selected_space, term_months, start_date):
        lease: Lease | None = self.repo.get_by_id_and_tenant(tenant_id=tenant_id, lease_id=lease_id)
        if lease is None:
            raise LookupError("failed to find lease")

        lease.activate_lease(
            selected_space=selected_space,
            term_months = term_months,
            start_date = start_date
        )

        # need to check for allocation space from capacity app
        self.repo.activate(lease=lease)

        return lease
