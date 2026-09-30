from abc import ABC, abstractmethod


class TenantRepository(ABC):
    @abstractmethod
    def get(self, tenant_id): ...

    @abstractmethod
    def save(self, tenant): ...


class LeaseCountChecker(ABC):
    @abstractmethod
    def count_active(self, tenant_id): ...
