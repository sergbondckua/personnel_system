from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from apps.organization.models import OrgUnit
    from apps.personnel.models import Person


class AssignmentQuerySet(models.QuerySet):
    """
    QuerySet для роботи з призначеннями військовослужбовців.
    """

    def active(self) -> models.QuerySet:
        """
        Повертає лише активні призначення.
        """
        return self.filter(is_active=True)

    def inactive(self) -> models.QuerySet:
        """
        Повертає лише неактивні призначення.
        """
        return self.filter(is_active=False)

    def current(self) -> models.QuerySet:
        """
        Повертає поточні призначення.
        """
        return self.active()

    def for_person(self, person: Person) -> models.QuerySet:
        """
        Повертає всі призначення військовослужбовця.
        """
        return self.filter(person=person)

    def for_unit(self, org_unit: OrgUnit) -> models.QuerySet:
        """
        Повертає всі активні призначення підрозділу.
        """
        return self.active().filter(
            staff_position__org_unit=org_unit,
        )

    def with_related(self) -> models.QuerySet:
        """
        Завантажує пов'язані моделі одним SQL-запитом.
        """
        return self.select_related(
            "person",
            "staff_position",
            "staff_position__org_unit",
        )


AssignmentManager = models.Manager.from_queryset(AssignmentQuerySet)
