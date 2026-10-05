from abc import ABC, abstractmethod

from users.core.domain.entities.tenant import Tenant


class TenantPort(ABC):
    @abstractmethod
    def get(self, tenant_id) -> Tenant: ...

    @abstractmethod
    def save(self, tenant) -> None: ...

    @abstractmethod
    def count_active_leases(self, tenant_id) -> int: ...

    @abstractmethod
    def create(self, user_id, company_name) -> Tenant: ...

    @abstractmethod
    def list_all(self) -> list[Tenant]: ...
