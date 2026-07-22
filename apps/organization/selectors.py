from __future__ import annotations

from django.db.models import Sum

from apps.organization.models import OrgUnit, StaffPosition


class OrganizationSelector:
    """
    ORM-запити для роботи зі структурою організації.
    """

    @staticmethod
    def staff_positions(org_unit: OrgUnit):
        """
        Повертає всі активні штатні посади підрозділу.
        """
        return StaffPosition.objects.filter(
            org_unit=org_unit,
            is_active=True,
        )

    @staticmethod
    def staff_count(org_unit: OrgUnit) -> int:
        """
        Повертає штатну чисельність підрозділу.
        """
        return (
            StaffPosition.objects.filter(
                org_unit=org_unit,
                is_active=True,
            ).aggregate(total=Sum("staff_count"))["total"]
            or 0
        )

    @staticmethod
    def root_units():
        """
        Повертає всі кореневі підрозділи.
        """
        return (
            OrgUnit.objects.filter(parent__isnull=True)
            .select_related(
                "organization",
                "type",
            )
            .prefetch_related(
                "children",
            )
            .order_by(
                "organization",
                "sort_order",
                "name",
            )
        )

    @staticmethod
    def personnel(org_unit: OrgUnit):
        """
        Повертає військовослужбовців, які зараз проходять службу
        в зазначеному підрозділі.
        """
        from apps.assignments.models import Assignment

        return (
            Assignment.objects.filter(
                is_active=True,
                staff_position__org_unit=org_unit,
            )
            .select_related(
                "person",
                "staff_position",
                "person__military_rank",
            )
            .order_by(
                "staff_position__position_number",
                "person__last_name",
                "person__first_name",
            )
        )
