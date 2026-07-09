from django.db.models import Count, Q

from apps.organization.models import StaffPosition


class StaffingService:
    """
    Сервіс роботи зі штатною укомплектованістю.
    """

    @staticmethod
    def staffed_count(position: StaffPosition) -> int:
        """
        Кількість зайнятих штатних одиниць.
        """
        return position.assignments.filter(
            is_active=True,
        ).count()

    @staticmethod
    def vacant_count(position: StaffPosition) -> int:
        """
        Кількість вакантних штатних одиниць.
        """
        return max(
            position.staff_count - StaffingService.staffed_count(position),
            0,
        )

    @staticmethod
    def staffing_percent(position: StaffPosition) -> float:
        """
        Відсоток укомплектованості.
        """
        if position.staff_count == 0:
            return 0.0

        return round(
            StaffingService.staffed_count(position)
            / position.staff_count
            * 100,
            1,
        )

    @staticmethod
    def annotate(queryset):
        """
        Додає кількість призначень до queryset.
        """
        return queryset.annotate(
            staffed=Count(
                "assignments",
                filter=Q(assignments__is_active=True),
            ),
        )
