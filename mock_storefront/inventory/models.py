from django.db import models

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    lease_id = models.UUIDField()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    format_type = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    thickness = models.DecimalField(max_digits=6, decimal_places=2)
    unit_weight = models.DecimalField(max_digits=8, decimal_places=3)
    quantity = models.PositiveIntegerField()
    unit_volume = models.DecimalField(max_digits=14, decimal_places=2)
    total_volume = models.DecimalField(max_digits=20, decimal_places=2)
    total_weight = models.DecimalField(max_digits=14, decimal_places=3)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
