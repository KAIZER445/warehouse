from django.db import models

class Role(models.TextChoices):
    TENANT = 'tenant', 'Tenant'
    OPS = 'ops', 'Ops'
    ADMIN = 'admin', 'Admin'