from django.db import models

from apps.common.models import BaseModel
from apps.personnel.models import Person
from apps.references.models import VacationType
from apps.vacations.enums import VacationStatus
from apps.vacations.services import VacationService


class Vacation(BaseModel):
    """
    Відпустка військовослужбовця.
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="vacations",
        verbose_name="Військовослужбовець",
    )

    vacation_type = models.ForeignKey(
        VacationType,
        on_delete=models.PROTECT,
        related_name="vacations",
        verbose_name="Вид відпустки",
    )

    date_from = models.DateField(
        verbose_name="Дата початку",
    )

    date_to = models.DateField(
        verbose_name="Дата закінчення",
    )

    days = models.PositiveSmallIntegerField(
        verbose_name="Кількість діб",
    )

    order_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер наказу",
    )

    order_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата наказу",
    )

    status = models.CharField(
        max_length=15,
        choices=VacationStatus.choices,
        default=VacationStatus.PLANNED,
        verbose_name="Статус",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітки",
    )

    class Meta:
        db_table = "vacation"
        verbose_name = "Відпустка"
        verbose_name_plural = "Відпустки"

        constraints = [
            models.CheckConstraint(
                condition=models.Q(date_to__gte=models.F("date_from")),
                name="ck_vacation_dates",
            ),
            models.CheckConstraint(
                condition=models.Q(days__gt=0),
                name="ck_vacation_days_gt_0",
            ),
        ]

    def clean(self) -> None:
        """
        Виконує бізнес-перевірки перед збереженням.
        """
        super().clean()

    def save(self, *args, **kwargs):
        VacationService.validate(self)
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.person} ({self.date_from} - {self.date_to})"
