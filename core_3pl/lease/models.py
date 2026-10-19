from django.db import models
from config.models import BaseModel
from lease.core.domain.enum import LeaseStatus
from users.models import Tenant as TenantModel


class Lease(BaseModel):
    tenant = models.ForeignKey(
        TenantModel, on_delete=models.PROTECT, related_name="leases"
    )
    box_combination = models.JSONField()
    total_boxes = models.PositiveIntegerField()
    minimum_required_space = models.DecimalField(max_digits=12, decimal_places=5)
    total_volume = models.DecimalField(max_digits=12, decimal_places=5)
    total_weight = models.DecimalField(max_digits=12, decimal_places=5)
    status = models.CharField(
        max_length=20, choices=LeaseStatus.choices, default=LeaseStatus.PENDING
    )
    selected_space = models.DecimalField(
        max_digits=12, decimal_places=5, null=True, blank=True
    )
    term_months = models.PositiveSmallIntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
