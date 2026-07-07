from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.organization.models import Organization, OrgUnitType, OrgUnit


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
    Адміністрування типів підрозділів.
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
