from django.db import models


class BaseModel(models.Model):
    """Базовий клас для всіх моделей"""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Створено",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Оновлено",
    )

    class Meta:
        abstract = True
