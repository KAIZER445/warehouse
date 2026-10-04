from abc import ABC, abstractmethod


class TenantPort(ABC):
    @abstractmethod
    def get(self, tenant_id): ...

    @abstractmethod
    def save(self, tenant): ...

    @abstractmethod
    def count_active_leases(self, tenant_id): ...
