from users.core.domain.ports import TenantPort, TenantServicePort


class TenantService(TenantServicePort):
    def __init__(self, repo: TenantPort):
        self.repo = repo

    def deactivate(self, tenant_id):
        tenant = self.repo.get(tenant_id)
        tenant.deactivate(self.repo.count_active_leases(tenant.id))
        self.repo.save(tenant)

    def list_all(self):
        return self.repo.list_all()