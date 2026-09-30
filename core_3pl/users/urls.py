from django.urls import path

from .views import ListOps, ListTenants, ListUsers, RegisterUser

urlpatterns = [
    path("list/", ListUsers.as_view()),
    path("list/tenants/", ListTenants.as_view()),
    path("list/ops/", ListOps.as_view()),
    path("register/", RegisterUser.as_view()),
]
