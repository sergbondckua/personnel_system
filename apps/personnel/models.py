from django.db import models

from apps.common.models import BaseModel
from apps.references.models import (
    MilitaryRank,
    MilitarySpecialty,
    PersonnelCategory,
)


class Person(BaseModel):
    """
    Особова картка військовослужбовця.
    """

    last_name = models.CharField(
        max_length=100,
        verbose_name="Прізвище",
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name="Ім'я",
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="По батькові",
    )

    service_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Особовий номер",
    )

    birth_date = models.DateField(
        verbose_name="Дата народження",
    )

    military_rank = models.ForeignKey(
        MilitaryRank,
        on_delete=models.PROTECT,
        related_name="persons",
        verbose_name="Військове звання",
    )

    military_specialty = models.ForeignKey(
        MilitarySpecialty,
        on_delete=models.PROTECT,
        related_name="persons",
        verbose_name="Військово-облікова спеціальність",
    )

    personnel_category = models.ForeignKey(
        PersonnelCategory,
        on_delete=models.PROTECT,
        related_name="persons",
        verbose_name="Категорія особового складу",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Проходить службу",
    )

    class Meta:
        db_table = "person"
        verbose_name = "Військовослужбовець"
        verbose_name_plural = "Військовослужбовці"

    def __str__(self) -> str:
        return (
            f"{self.last_name} {self.first_name} {self.middle_name}"
        ).strip()
