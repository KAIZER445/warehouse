from abc import ABC, abstractmethod

from users.core.domain.entities.tenant import Tenant


class TenantServicePort(ABC):
    @abstractmethod
    def deactivate(self, tenant_id) -> None: ...

    @abstractmethod
    def list_all(self) -> list[Tenant]: ...