from django.contrib import admin

from apps.common.admin import BaseAdmin
from apps.personnel.models import Person


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    """
    Адміністрування особових карток військовослужбовців.
    """

    list_display = (
        "service_number",
        "last_name",
        "first_name",
        "middle_name",
        "military_rank",
        "personnel_category",
        "is_active",
    )

    list_filter = (
        "is_active",
        "military_rank",
        "personnel_category",
    )

    search_fields = (
        "service_number",
        "last_name",
        "first_name",
        "middle_name",
    )

    autocomplete_fields = (
        "military_rank",
        "military_specialty",
        "personnel_category",
    )

    list_select_related = (
        "military_rank",
        "military_specialty",
        "personnel_category",
    )

    ordering = (
        "last_name",
        "first_name",
        "middle_name",
    )
