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

    type = models.ForeignKey(
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
        return f"{self.type} {self.name}"


class StaffPosition(BaseModel):
    """
    Штатна посада.

    Описує посаду штатного розпису в конкретному структурному підрозділі.
    """

    org_unit = models.ForeignKey(
        OrgUnit,
        on_delete=models.CASCADE,
        related_name="staff_positions",
        verbose_name="Підрозділ",
    )

    position_number = models.CharField(
        max_length=20,
        verbose_name="Номер за штатом",
        help_text="Номер посади відповідно до штатного розпису.",
    )

    name = models.CharField(
        max_length=250,
        verbose_name="Назва посади",
    )

    military_rank = models.ForeignKey(
        MilitaryRank,
        on_delete=models.PROTECT,
        related_name="staff_positions",
        verbose_name="Граничне військове звання",
    )

    military_specialty = models.ForeignKey(
        MilitarySpecialty,
        on_delete=models.PROTECT,
        related_name="staff_positions",
        verbose_name="Військово-облікова спеціальність",
    )

    personnel_category = models.ForeignKey(
        PersonnelCategory,
        on_delete=models.PROTECT,
        related_name="staff_positions",
        verbose_name="Категорія особового складу",
    )

    tariff_grade = models.ForeignKey(
        TariffGrade,
        on_delete=models.PROTECT,
        related_name="staff_positions",
        null=True,
        blank=True,
        verbose_name="Тарифний розряд",
    )

    staff_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Кількість штатних одиниць",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітки",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        db_table = "staff_position"
        verbose_name = "Штатна посада"
        verbose_name_plural = "Штатні посади"

        constraints = [
            models.UniqueConstraint(
                fields=("org_unit", "position_number"),
                name="uq_staff_position_org_unit_position_number",
            ),
            models.CheckConstraint(
                condition=models.Q(staff_count__gt=0),
                name="ck_staff_position_staff_count_gt_0",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.position_number} - {self.name}"
