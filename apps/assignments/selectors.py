from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps
from django.db.models import QuerySet

if TYPE_CHECKING:
    from apps.organization.models import OrgUnit
    from apps.personnel.models import Person
    from apps.assignments.models import Assignment

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
        return Assignment.objects.for_unit(org_unit).with_related()

    @staticmethod
    def active_count_by_unit(org_unit: OrgUnit) -> int:
        """
        Повертає кількість активних призначень у підрозділі.
        """
        return Assignment.objects.for_unit(org_unit).count()
