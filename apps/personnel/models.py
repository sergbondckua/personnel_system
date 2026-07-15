from django.db import models

from apps.common.models import BaseModel
from apps.personnel.enums import Sex
from apps.personnel.utils import person_photo_upload_path
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

    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
        default=Sex.MALE,
        verbose_name="Стать",
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

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Електронна пошта",
    )

    photo = models.ImageField(
        upload_to=person_photo_upload_path,
        blank=True,
        null=True,
        verbose_name="Фотографія",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітки",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Проходить службу",
    )

    class Meta:
        db_table = "person"
        verbose_name = "Військовослужбовець"
        verbose_name_plural = "Військовослужбовці"

        indexes = [
            models.Index(fields=("last_name", "first_name")),
            models.Index(fields=("service_number",)),
            models.Index(fields=("is_active",)),
        ]

    @property
    def full_name(self) -> str:
        """
        Повертає повне ПІБ.
        """
        return " ".join(
            filter(
                None,
                (
                    self.last_name,
                    self.first_name,
                    self.middle_name,
                ),
            )
        )

    @property
    def short_name(self) -> str:
        """
        Повертає скорочене ПІБ.

        Наприклад:
        Петренко Сергій Петрович →
        Петренко С.П.
        """
        initials = []

        if self.first_name:
            initials.append(f"{self.first_name[0]}.")

        if self.middle_name:
            initials.append(f"{self.middle_name[0]}.")

        return f"{self.last_name} {' '.join(initials)}".strip()

    def __str__(self) -> str:
        return self.full_name
