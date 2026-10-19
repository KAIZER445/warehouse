from django.db import models
from dataclasses import dataclass
from enum import Enum


class LeaseStatus(models.TextChoices):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    ENDED = "ENDED"


@dataclass(frozen=True)
class Dimensions:
    length: int
    width: int
    height: int


class BoxSize(Enum):
    SMALL = Dimensions(30, 20, 20)
    MEDIUM = Dimensions(40, 30, 30)
    LARGE = Dimensions(60, 40, 40)
