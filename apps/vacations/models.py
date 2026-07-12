from django.db import models

from apps.common.models import BaseModel
from apps.personnel.models import Person
from apps.references.models import VacationType
from apps.vacations.enums import VacationStatus


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
        editable=False,
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
        Виконує підготовку моделі до валідації.
        """
        super().clean()

        if self.date_from and self.date_to:
            self.days = (self.date_to - self.date_from).days + 1

        from apps.vacations.services import VacationService

        VacationService.validate(self)

    def save(self, *args, **kwargs) -> None:
        """
        Зберігає відпустку.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.person} ({self.date_from} - {self.date_to})"
