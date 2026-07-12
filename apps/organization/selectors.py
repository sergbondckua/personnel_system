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
