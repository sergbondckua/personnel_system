from django.contrib import admin

from apps.assignments.models import Assignment
from apps.common.admin import BaseAdmin


@admin.register(Assignment)
class AssignmentAdmin(BaseAdmin):
    """
    Адміністрування призначень військовослужбовців.
    """

    list_display = (
        "person",
        "staff_position",
        "date_from",
        "date_to",
        "is_active",
    )

    list_filter = (
        "is_active",
        "staff_position__org_unit__organization",
        "staff_position__org_unit",
    )

    search_fields = (
        "person__service_number",
        "person__last_name",
        "person__first_name",
        "staff_position__position_number",
        "staff_position__name",
        "order_number",
    )

    autocomplete_fields = (
        "person",
        "staff_position",
    )

    list_select_related = (
        "person",
        "staff_position",
        "staff_position__org_unit",
    )

    ordering = (
        "-is_active",
        "-date_from",
        "person__last_name",
    )
