from abc import ABC, abstractmethod
from uuid import UUID

from lease.core.domain.book import Book
from lease.core.domain.entity import Lease

class Lease(ABC):

    @abstractmethod
    def save(self, lease: Lease, books: list[Book]) -> UUID: ...

    @abstractmethod
    def get_by_id_and_tenant(self, lease_id: UUID, tenant_id: UUID) -> Lease | None: ...

    @abstractmethod
    def activate(self, lease: Lease): ...

    @abstractmethod
    def list_by_tenant(self, tenant_id: UUID) -> list[Lease]: ...