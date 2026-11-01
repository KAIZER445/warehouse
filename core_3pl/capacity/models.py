import uuid
from decimal import Decimal
from django.db import models

class Capacity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    total_capacity = models.DecimalField(max_digits=14, decimal_places=5, default=Decimal("0.00000"))
    current_allocated_space = models.DecimalField(max_digits=14, decimal_places=5, default=Decimal("0.00000"))
