from django.db import models

class Operators(models.TextChoices):
    ADDITION = "addition", "Addition"
    SUBTRACTION = "subtraction", "Subtraction"
