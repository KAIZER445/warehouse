from rest_framework.permissions import BasePermission
from users.enums import Role

class IsOps(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.OPS
        )

class IsTenant(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == Role.TENANT
        )
