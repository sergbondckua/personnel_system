from django.db import models


class BaseModel(models.Model):
    """Базовий клас для всіх моделей"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
