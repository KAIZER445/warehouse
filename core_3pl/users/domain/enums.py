from django.db import models


class Role(models.TextChoices):
    TENANT = "tenant", "Tenant"
    OPS = "ops", "Ops"
    ADMIN = "admin", "Admin"


class Department(models.TextChoices):
    CAPACITY_MANAGEMENT = "capacity_management", "Capacity_Management"
    CUSTOMER_SUPPORT = "customer_support", "Customer_Support"
