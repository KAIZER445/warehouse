from config.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from .domain.enums import Department, Role


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.last_login = timezone.now()
        user.save()
        return user


class User(BaseModel, AbstractBaseUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        null=False,
        blank=False,
        default=Role.TENANT,
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Ops(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(unique=True, max_length=255, null=False, blank=False)
    department = models.CharField(
        max_length=20,
        choices=Department.choices,
        default=Department.CUSTOMER_SUPPORT,
        null=False,
        blank=False,
    )


class Tenant(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(
        unique=True, max_length=255, null=False, blank=False
    )
