from django.db import models

from apps.common.models import BaseModel
from apps.organization.models import StaffPosition
from apps.personnel.models import Person


class Assignment(BaseModel):
    """
    Призначення військовослужбовця на штатну посаду.
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Військовослужбовець",
    )

    staff_position = models.ForeignKey(
        StaffPosition,
        on_delete=models.PROTECT,
        related_name="assignments",
        verbose_name="Штатна посада",
    )

    date_from = models.DateField(
        verbose_name="Дата призначення",
    )

    date_to = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата звільнення з посади",
    )

    order_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер наказу",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітки",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Поточне призначення",
    )

    class Meta:
        db_table = "assignment"
        verbose_name = "Призначення"
        verbose_name_plural = "Призначення"

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(date_to__isnull=True)
                    | models.Q(date_to__gte=models.F("date_from"))
                ),
                name="ck_assignment_dates",
            ),
            models.UniqueConstraint(
                fields=("person",),
                condition=models.Q(is_active=True),
                name="uq_assignment_person_active",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.person} → {self.staff_position} ({self.date_from})"
