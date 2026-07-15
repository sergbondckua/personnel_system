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
        "service_number",
        "organization",
        "org_unit",
        "staff_position",
        "date_from",
        "date_to",
        "is_active",
    )

    list_display_links = (
        "person",
        "staff_position",
    )

    search_fields = (
        "person__service_number",
        "person__last_name",
        "person__first_name",
        "person__middle_name",
        "staff_position__position_number",
        "staff_position__name",
    )

    list_filter = (
        "is_active",
        "staff_position__org_unit__organization",
        "staff_position__org_unit",
        "staff_position__military_rank",
        "staff_position__personnel_category",
    )

    ordering = (
        "-is_active",
        "-date_from",
        "person__last_name",
    )

    autocomplete_fields = (
        "person",
        "staff_position",
    )

    list_select_related = (
        "person",
        "staff_position",
        "staff_position__org_unit",
        "staff_position__org_unit__organization",
        "staff_position__military_rank",
        "staff_position__personnel_category",
    )

    fieldsets = (
        (
            "Основні дані",
            {
                "fields": (
                    "person",
                    "staff_position",
                    "date_from",
                    "date_to",
                    "is_active",
                ),
            },
        ),
        (
            "Документ",
            {
                "fields": (
                    "order_number",
                    "notes",
                ),
            },
        ),
    ) + BaseAdmin.fieldsets

    @admin.display(
        ordering="person__service_number",
        description="Особовий №",
    )
    def service_number(self, obj: Assignment) -> str:
        """
        Повертає особовий номер військовослужбовця.
        """
        return obj.person.service_number

    @admin.display(
        ordering="staff_position__org_unit__organization__short_name",
        description="Організація",
    )
    def organization(self, obj: Assignment) -> str:
        """
        Повертає організацію.
        """
        return str(obj.staff_position.org_unit.organization)

    @admin.display(
        ordering="staff_position__org_unit__name",
        description="Підрозділ",
    )
    def org_unit(self, obj: Assignment) -> str:
        """
        Повертає структурний підрозділ.
        """
        return str(obj.staff_position.org_unit.full_name)
