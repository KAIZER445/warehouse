from django.db import models

class LeaseStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

class BoxSizes(models.TextChoices)