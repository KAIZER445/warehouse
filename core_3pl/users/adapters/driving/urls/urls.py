from django.urls import path

from users.adapters.driving.views import ListOps, ListTenants, ListUsers, RegisterUser, DeactivateTenant

urlpatterns = [
    path("list/", ListUsers.as_view()),
    path("list/tenants/", ListTenants.as_view()),
    path("list/ops/", ListOps.as_view()),
    path("register/", RegisterUser.as_view()),
    path("tenants/<int:tenant_id>/deactivate/", DeactivateTenant.as_view()),
]
