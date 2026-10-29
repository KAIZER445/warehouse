from lease.core.domain.ports_service import LeaseServicePort
from lease.core.domain.ports import Lease as LeasePort
from lease.core.domain.entity import Lease
from lease.core.domain.dto import QuoteResult

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
