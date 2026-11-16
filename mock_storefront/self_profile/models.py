from django.db import models


class SelfProfile(models.Model):
    company_name = models.CharField(unique=True, max_length=255)
    base_url = models.CharField(unique=True, max_length=255)
    encrypted_secret = models.CharField(max_length=1024, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
