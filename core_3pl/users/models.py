from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .enums import Role
from django.utils import timezone
from config.models import BaseModel

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
    role = models.CharField(max_length=20, choices=Role.choices, null=False, blank=False, default=Role.TENANT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()