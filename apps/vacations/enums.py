from django.db import models


class VacationStatus(models.TextChoices):
    """
    Статуси відпустки.
    """

    PLANNED = "planned", "Запланована"
    APPROVED = "approved", "Погоджена"
    ACTIVE = "active", "У відпустці"
    COMPLETED = "completed", "Завершена"
    CANCELED = "canceled", "Скасована"
