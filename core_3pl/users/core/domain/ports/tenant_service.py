from abc import ABC, abstractmethod


class TenantServicePort(ABC):
    @abstractmethod
    def deactivate(self, tenant_id): ...