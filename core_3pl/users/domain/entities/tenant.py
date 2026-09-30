class Tenant:
    def __init__(self, id, user_id, company_name, is_active, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.company_name = company_name
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def deactivate(self, active_lease_count):
        if active_lease_count > 0:
            raise ValueError("Tenant has a active leases")
        self.is_active = False
