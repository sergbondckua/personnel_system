from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps
from django.db.models import QuerySet

if TYPE_CHECKING:
    from apps.assignments.models import Assignment
    from apps.organization.models import OrgUnit
    from apps.personnel.models import Person

Assignment = apps.get_model("assignments", "Assignment")


class AssignmentSelector:
    """
    ORM-запити для роботи з призначеннями військовослужбовців.

    Selector не містить бізнес-логіки та використовується
    виключно для отримання даних із бази.
    """

    @staticmethod
    def current(person: Person):
        """
        Повертає поточне активне призначення військовослужбовця.
        """
        return (
            Assignment.objects.current()
            .for_person(person)
            .with_related()
            .first()
        )

    @staticmethod
    def active_by_unit(org_unit: OrgUnit) -> QuerySet:
        """
        Повертає всі активні призначення підрозділу.
        """
        return (
            Assignment.objects.for_unit(org_unit)
            .with_related()
            .order_by(
                "staff_position__position_number",
                "person__last_name",
                "person__first_name",
            )
        )

    @staticmethod
    def active_count_by_unit(org_unit: OrgUnit) -> int:
        """
        Повертає кількість активних військовослужбовців
        у підрозділі.
        """
        return Assignment.objects.for_unit(org_unit).count()

    @staticmethod
    def all_active() -> QuerySet:
        """
        Повертає всі активні призначення.

        Використовується для побудови дерева особового складу,
        графіка відпусток та інших кадрових екранів.
        """
        return (
            Assignment.objects.current()
            .with_related()
            .order_by(
                "staff_position__org_unit__organization",
                "staff_position__org_unit__sort_order",
                "staff_position__position_number",
                "person__last_name",
                "person__first_name",
            )
        )