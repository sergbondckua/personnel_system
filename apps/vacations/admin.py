from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.vacations.models import Vacation


@admin.register(Vacation)
class VacationAdmin(BaseAdmin):
    """
    Адміністрування відпусток.
    """

    list_display = (
        "person",
        "vacation_type",
        "date_from",
        "date_to",
        "days",
        "status",
    )

    list_filter = (
        "status",
        "vacation_type",
    )

    search_fields = (
        "person__last_name",
        "person__first_name",
        "person__service_number",
        "order_number",
    )

    autocomplete_fields = (
        "person",
        "vacation_type",
    )

    list_select_related = (
        "person",
        "vacation_type",
    )

    ordering = ("-date_from",)
