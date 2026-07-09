from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.organization.services import StaffingService
from apps.organization.models import (
    Organization,
    OrgUnit,
    OrgUnitType,
    StaffPosition,
)


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

    search_fields = (
        "short_name",
        "full_name",
        "code",
    )

    ordering = ("short_name",)


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

    search_fields = (
        "name",
        "short_name",
    )

    ordering = ("sort_order",)


@admin.register(OrgUnit)
class OrgUnitAdmin(BaseAdmin):
    """
    Адміністрування структурних підрозділів.
    """

    list_display = (
        "name",
        "type",
        "organization",
        "parent",
        "is_active",
    )

    list_filter = (
        "organization",
        "type",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
        "code",
    )

    autocomplete_fields = (
        "organization",
        "parent",
        "type",
    )

    ordering = (
        "organization",
        "sort_order",
        "name",
    )


@admin.register(StaffPosition)
class StaffPositionAdmin(BaseAdmin):
    """
    Адміністрування штатних посад.
    """

    list_display = (
        "position_number",
        "name",
        "org_unit",
        "staff_count",
        "staffed",
        "vacant",
        "staffing",
        "is_active",
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
        "military_specialty__code",
        "military_specialty__name",
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
        "military_rank",
        "military_specialty",
        "personnel_category",
        "tariff_grade",
    )

    ordering = (
        "org_unit",
        "position_number",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return StaffingService.annotate(queryset)

    @admin.display(description="Зайнято")
    def staffed(self, obj):
        return obj.staffed

    @admin.display(description="Вакантно")
    def vacant(self, obj):
        return obj.staff_count - obj.staffed

    @admin.display(description="Укомплектованість")
    def staffing(self, obj):
        if obj.staff_count == 0:
            return "0 %"

        percent = round(obj.staffed / obj.staff_count * 100, 1)

        return f"{percent} %"


