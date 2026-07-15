from django.contrib import admin
from django.db.models import QuerySet

from apps.common.admin import BaseAdmin
from apps.organization.models import (
    Organization,
    OrgUnit,
    OrgUnitType,
    StaffPosition,
)
from apps.organization.services import StaffingService


@admin.register(Organization)
class OrganizationAdmin(BaseAdmin):
    """
    Адміністрування організацій.
    """

    list_display = (
        "short_name",
        "full_name",
        "code",
    )

    list_display_links = ("short_name",)

    search_fields = (
        "short_name",
        "full_name",
        "code",
    )

    ordering = ("short_name",)

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "short_name",
                    "full_name",
                    "code",
                ),
            },
        ),
        *BaseAdmin.fieldsets,
    )


@admin.register(OrgUnitType)
class OrgUnitTypeAdmin(BaseAdmin):
    """
    Адміністрування типів структурних підрозділів.
    """

    list_display = (
        "name",
        "short_name",
        "sort_order",
    )

    list_display_links = ("name",)

    search_fields = (
        "name",
        "short_name",
    )

    ordering = (
        "sort_order",
        "name",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "name",
                    "short_name",
                    "sort_order",
                ),
            },
        ),
        *BaseAdmin.fieldsets,
    )


@admin.register(OrgUnit)
class OrgUnitAdmin(BaseAdmin):
    """
    Адміністрування структурних підрозділів.
    """

    list_display = (
        "full_name_display",
        "type",
        "organization",
        "code",
        "sort_order",
        "is_active",
    )

    list_display_links = ("full_name_display",)

    list_filter = (
        "organization",
        "type",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
        "code",
        "parent__name",
        "parent__short_name",
    )

    ordering = (
        "organization",
        "sort_order",
        "name",
    )

    autocomplete_fields = (
        "organization",
        "parent",
        "type",
    )

    list_select_related = (
        "organization",
        "parent",
        "type",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "organization",
                    "parent",
                    "type",
                ),
            },
        ),
        (
            "Назва",
            {
                "fields": (
                    "name",
                    "short_name",
                    "code",
                ),
            },
        ),
        (
            "Налаштування",
            {
                "fields": (
                    "sort_order",
                    "is_active",
                ),
            },
        ),
        *BaseAdmin.fieldsets,
    )

    @admin.display(
        description="Структурний підрозділ",
        ordering="name",
    )
    def full_name_display(self, obj: OrgUnit) -> str:
        """
        Повертає повний шлях структурного підрозділу.
        """
        return obj.full_name


@admin.register(StaffPosition)
class StaffPositionAdmin(BaseAdmin):
    """
    Адміністрування штатних посад.
    """

    list_display = (
        "position_number",
        "name",
        "org_unit_display",
        "military_rank",
        "personnel_category",
        "staff_count",
        "staffed",
        "vacant",
        "staffing",
        "is_active",
    )

    list_display_links = (
        "position_number",
        "name",
    )

    list_filter = (
        "is_active",
        "org_unit__organization",
        "org_unit__type",
        "personnel_category",
        "military_rank",
    )

    search_fields = (
        "position_number",
        "name",
        "org_unit__name",
        "org_unit__short_name",
        "military_specialty__code",
        "military_specialty__name",
    )

    ordering = (
        "org_unit__organization",
        "org_unit__sort_order",
        "position_number",
    )

    autocomplete_fields = (
        "org_unit",
        "military_rank",
        "military_specialty",
        "personnel_category",
        "tariff_grade",
    )

    list_select_related = (
        "org_unit",
        "org_unit__parent",
        "org_unit__organization",
        "military_rank",
        "military_specialty",
        "personnel_category",
        "tariff_grade",
    )

    fieldsets = (
        (
            "Основна інформація",
            {
                "fields": (
                    "org_unit",
                    "position_number",
                    "name",
                ),
            },
        ),
        (
            "Штатні параметри",
            {
                "fields": (
                    "military_rank",
                    "military_specialty",
                    "personnel_category",
                    "tariff_grade",
                    "staff_count",
                ),
            },
        ),
        (
            "Додаткова інформація",
            {
                "fields": (
                    "notes",
                    "is_active",
                ),
            },
        ),
        *BaseAdmin.fieldsets,
    )

    def get_queryset(self, request) -> QuerySet[StaffPosition]:
        """
        Повертає список посад з інформацією
        про кількість зайнятих штатних одиниць.
        """
        queryset = super().get_queryset(request)
        return StaffingService.annotate(queryset)

    @admin.display(
        description="Підрозділ",
        ordering="org_unit__name",
    )
    def org_unit_display(self, obj: StaffPosition) -> str:
        """
        Повертає повний шлях структурного підрозділу.
        """
        return obj.org_unit.full_name

    @admin.display(
        description="Зайнято",
        ordering="staffed",
    )
    def staffed(self, obj: StaffPosition) -> int:
        """
        Повертає кількість зайнятих штатних одиниць.
        """
        return obj.staffed

    @admin.display(
        description="Вакантно",
    )
    def vacant(self, obj: StaffPosition) -> int:
        """
        Повертає кількість вакантних штатних одиниць.
        """
        return obj.staff_count - obj.staffed

    @admin.display(
        description="Укомплектованість",
    )
    def staffing(self, obj: StaffPosition) -> str:
        """
        Повертає відсоток укомплектованості штатної посади.
        """
        if obj.staff_count == 0:
            return "0 %"

        percent = round((obj.staffed / obj.staff_count) * 100, 1)
        return f"{percent} %"
