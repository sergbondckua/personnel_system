from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.references.models import (
    MilitaryRank,
    MilitarySpecialty,
    PersonnelCategory,
    TariffGrade,
    VacationType,
)


@admin.register(MilitaryRank)
class MilitaryRankAdmin(BaseAdmin):
    """
    Адміністрування військових звань.
    """

    list_display = (
        "short_name",
        "name",
        "order",
    )

    search_fields = (
        "name",
        "short_name",
    )

    ordering = ("order",)


@admin.register(MilitarySpecialty)
class MilitarySpecialtyAdmin(BaseAdmin):
    """
    Адміністрування військово-облікових спеціальностей.
    """

    list_display = (
        "code",
        "name",
    )

    search_fields = (
        "code",
        "name",
    )

    ordering = ("code",)


@admin.register(PersonnelCategory)
class PersonnelCategoryAdmin(BaseAdmin):
    """
    Адміністрування категорій особового складу.
    """

    list_display = (
        "short_name",
        "name",
    )

    search_fields = (
        "name",
        "short_name",
    )


@admin.register(TariffGrade)
class TariffGradeAdmin(BaseAdmin):
    """
    Адміністрування тарифних розрядів.
    """

    list_display = ("number",)

    search_fields = ("number",)

    ordering = ("number",)


@admin.register(VacationType)
class LeaveTypeAdmin(BaseAdmin):
    """
    Адміністрування видів відпусток.
    """

    list_display = (
        "name",
        "annual_limit",
        "is_active",
    )

    list_filter = ("is_active",)

    search_fields = (
        "name",
        "short_name",
    )

    ordering = ("name",)
