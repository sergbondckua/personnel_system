from apps.assignments.models import Assignment
from apps.common.admin import ReadOnlyInline
from apps.vacations.models import Vacation


class AssignmentInline(ReadOnlyInline):
    """
    Історія призначень військовослужбовця.
    """

    model = Assignment

    fields = (
        "staff_position",
        "date_from",
        "date_to",
        "is_active",
    )

    readonly_fields = fields

    ordering = (
        "-is_active",
        "-date_from",
    )

    verbose_name = "Призначення"

    verbose_name_plural = "Історія призначень"


class VacationInline(ReadOnlyInline):
    """
    Історія відпусток військовослужбовця.
    """

    model = Vacation

    fields = (
        "vacation_type",
        "date_from",
        "date_to",
        "status",
    )

    readonly_fields = fields

    ordering = ("-date_from",)

    verbose_name = "Відпустка"

    verbose_name_plural = "Історія відпусток"
