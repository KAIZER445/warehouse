import uuid

from django.db import models

class WareHouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    total_capacity = models.PositiveIntegerField(default=0)
    current_allocated_space = models.PositiveIntegerField(default=0)