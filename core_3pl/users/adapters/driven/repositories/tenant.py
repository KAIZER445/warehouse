from users.core.domain.ports import TenantPort
from users.models import Tenant, User

from ..mappers.tenant import to_entity


class TenantRepository(TenantPort):
    def get(self, tenant_id):
        row = Tenant.objects.select_related("user").get(id=tenant_id)
        return to_entity(row)

    def save(self, tenant):
        User.objects.filter(id=tenant.user_id).update(is_active=tenant.is_active)

    def count_active_leases(self, tenant_id):
        # TODO: Wire up once the leasing app is built
        # from leasing.models import SpaceLease
        # return SpaceLease.objects.filter(tenant_id=tenant_id, status="ACTIVE").count()
        return 0

    def create(self, user_id, company_name):
        row = Tenant.objects.create(user_id=user_id, company_name=company_name)
        row = Tenant.objects.select_related("user").get(id=row.id)
        return to_entity(row)

    def list_all(self):
        return [to_entity(row) for row in Tenant.objects.select_related("user").all()]