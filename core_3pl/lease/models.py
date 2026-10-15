from django.db import models
from config.models import BaseModel
from lease.core.domain.enum import LeaseStatus
from users.models import Tenant as TenantModel

class Lease(BaseModel):
    tenant = models.ForeignKey(TenantModel, on_delete=models.PROTECT, related_name="leases")
    selected_space = models.PositiveIntegerField()
    minimum_required_space = models.PositiveIntegerField()
    total_volume = models.DecimalField(max_digits=12, decimal_places=5)
    total_weight = models.DecimalField(max_digits=12, decimal_places=5)
    term_months = models.IntegerField()
    status = models.CharField(max_length=20,choices = LeaseStatus.choices, default = LeaseStatus.INACTIVE)
    start_date = models.DateField()
    end_date = models.DateField()
