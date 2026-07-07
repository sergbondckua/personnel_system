from django.db import models

from apps.common.models import BaseModel
from apps.references.models import (
    MilitaryRank,
    MilitarySpecialty,
    PersonnelCategory,
    TariffGrade,
)


class Organization(BaseModel):
    """
    Організація (військова частина, навчальний центр тощо).
    """

    full_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Повна назва",
    )

    short_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Скорочена назва",
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Код",
        help_text="Наприклад: А1234",
    )

    class Meta:
        db_table = "organization"
        verbose_name = "Організація"
        verbose_name_plural = "Організації"
        ordering = ("short_name", "full_name")

    def __str__(self):
        return self.short_name or self.full_name


class OrgUnitType(BaseModel):
    """
    Довідник типів структурних підрозділів.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Назва",
    )

    short_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Скорочена назва",
    )

    sort_order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    class Meta:
        db_table = "org_unit_type"
        verbose_name = "Тип підрозділу"
        verbose_name_plural = "Типи підрозділів"
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.short_name or self.name


class OrgUnit(BaseModel):
    """ """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="org_units",
        verbose_name="Організація",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Батьківський підрозділ",
    )

    unit_type = models.ForeignKey(
        OrgUnitType,
        on_delete=models.PROTECT,
        related_name="org_units",
        verbose_name="Тип підрозділу",
    )

    name = models.CharField(
        max_length=300,
        verbose_name="Назва",
    )

    short_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Скорочена назва",
    )

    code = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Код",
        help_text="Внутрішній код підрозділу (за наявності).",
    )

    sort_order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Порядок сортування",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний",
    )

    class Meta:
        db_table = "org_unit"
        verbose_name = "Структурний підрозділ"
        verbose_name_plural = "Структурні підрозділи"
        ordering = (
            "sort_order",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "parent", "name"),
                name="uq_org_unit_parent_name",
            ),
        ]

    def __str__(self):
        return f"{self.unit_type} {self.name}"


class StaffPosition(BaseModel):
    """
    Рядок штатного розпису.
    """

    org_unit = models.ForeignKey(
        OrgUnit,
        on_delete=models.CASCADE,
        related_name="staff_positions",
        verbose_name="Підрозділ",
    )

    position_name = models.CharField(
        max_length=250,
        verbose_name="Назва посади",
    )

    position_index = models.PositiveIntegerField(
        verbose_name="№ за штатом",
    )

    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Кількість штатних одиниць",
    )

    military_rank = models.ForeignKey(
        MilitaryRank,
        on_delete=models.PROTECT,
    )

    military_specialty = models.ForeignKey(
        MilitarySpecialty,
        on_delete=models.PROTECT,
    )

    personnel_category = models.ForeignKey(
        PersonnelCategory,
        on_delete=models.PROTECT,
    )

    tariff_grade = models.ForeignKey(
        TariffGrade,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True, verbose_name="Примітки")

    class Meta:
        db_table = "staff_position"
        verbose_name = "Штатна посада"
        verbose_name_plural = "Штатні посади"
        ordering = (
            "org_unit",
            "position_index",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("org_unit", "position_index"),
                name="uq_staff_position_index",
            )
        ]

    def __str__(self):
        return f"{self.position_index}. {self.position_name}"
