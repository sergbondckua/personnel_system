from apps.assignments.models import Assignment


class AssignmentService:
    """
    Бізнес-логіка призначень.
    """

    @staticmethod
    def get_current(person):
        """
        Повертає поточне призначення військовослужбовця.
        """
        return (
            Assignment.objects.current()
            .filter(person=person)
            .select_related(
                "staff_position",
                "staff_position__org_unit",
            )
            .first()
        )