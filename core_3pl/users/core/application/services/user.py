from users.core.domain.enums import Role
from users.core.domain.ports import UserPort, UserServicePort, TenantPort, OpsPort


class UserService(UserServicePort):
    def __init__(self, user_repo: UserPort, tenant_repo: TenantPort, ops_repo: OpsPort):
        self.user_repo = user_repo
        self.tenant_repo = tenant_repo
        self.ops_repo = ops_repo

    def register(self, email, password, role, profile_data):
        user = self.user_repo.create(email=email, password=password, role=role)
        if role == Role.TENANT:
            self.tenant_repo.create(
                user_id=user.id, company_name=profile_data["company_name"]
            )
        elif role == Role.OPS:
            self.ops_repo.create(
                user_id=user.id,
                full_name=profile_data["full_name"],
                department=profile_data.get("department"),
            )
        return user

    def list_all(self):
        return self.user_repo.list_all()
