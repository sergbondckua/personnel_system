from __future__ import annotations

from django.db.models import Count, Q, QuerySet

from apps.assignments.services import AssignmentService
from apps.organization.models import OrgUnit, StaffPosition
from apps.organization.selectors import OrganizationSelector


class StaffingService:
    """
    Бізнес-логіка розрахунку укомплектованості.
    """

    @staticmethod
    def annotate(queryset: "QuerySet[StaffPosition]") -> "QuerySet[StaffPosition]":
        """
        Анотує queryset штатних посад кількістю фактично
        зайнятих (укомплектованих) одиниць.
        """
        return queryset.annotate(
            staffed=Count(
                "assignments",
                filter=Q(assignments__is_active=True),
                distinct=True,
            )
        )

    @staticmethod
    def get_staff_count(org_unit: OrgUnit) -> int:
        """
        Штатна чисельність.
        """
        return OrganizationSelector.staff_count(org_unit)

    @staticmethod
    def get_assigned_count(org_unit: OrgUnit) -> int:
        """
        Фактична кількість призначених військовослужбовців.
        """
        return AssignmentService.get_active_personnel_count(org_unit)

    @classmethod
    def get_vacancy_count(cls, org_unit: OrgUnit) -> int:
        """
        Кількість вакантних посад.
        """
        return max(
            0,
            cls.get_staff_count(org_unit) - cls.get_assigned_count(org_unit),
        )

    @classmethod
    def get_completion_percent(cls, org_unit: OrgUnit) -> float:
        """
        Відсоток укомплектованості.
        """
        staff = cls.get_staff_count(org_unit)

        if staff == 0:
            return 0.0

        return round(
            cls.get_assigned_count(org_unit) / staff * 100,
            2,
        )
