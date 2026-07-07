from django.db import models

from apps.common.models import BaseModel


class MilitaryRank(BaseModel):
    """
    Довідник військових звань.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    short_name = models.CharField(
        max_length=50, unique=True, verbose_name="Скорочена назва"
    )
    order = models.PositiveSmallIntegerField(
        unique=True, verbose_name="Порядок сортування"
    )

    class Meta:
        db_table = "military_rank"
        ordering = ("order",)
        verbose_name = "Військове звання"
        verbose_name_plural = "Військові звання"

    def __str__(self):
        return self.short_name


class MilitarySpecialty(BaseModel):
    """
    Довідник військово-облікових спеціальностей.
    """

    code = models.CharField(max_length=20, unique=True, verbose_name="Код ВОС")
    name = models.CharField(max_length=300, verbose_name="Назва")

    class Meta:
        db_table = "military_specialty"
        ordering = ("code",)
        verbose_name = "Військово-облікова спеціальність"
        verbose_name_plural = "Військово-облікові спеціальності"

    def __str__(self):
        return f"{self.code} — {self.name}"


class PersonnelCategory(BaseModel):
    """
    Довідник категорій особового складу.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    short_name = models.CharField(
        max_length=30, blank=True, verbose_name="Скорочена назва"
    )

    class Meta:
        db_table = "personnel_category"
        ordering = ("name",)
        verbose_name = "Категорія особового складу"
        verbose_name_plural = "Категорії особового складу"

    def __str__(self):
        return self.short_name or self.name


class TariffGrade(BaseModel):
    """
    Довідник тарифних розрядів.
    """

    number = models.PositiveSmallIntegerField(
        unique=True, verbose_name="Тарифний розряд"
    )

    class Meta:
        db_table = "tariff_grade"
        ordering = ("number",)
        verbose_name = "Тарифний розряд"
        verbose_name_plural = "Тарифні розряди"

    def __str__(self):
        return str(self.number)
