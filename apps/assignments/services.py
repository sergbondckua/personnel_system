from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

from apps.assignments.selectors import AssignmentSelector

if TYPE_CHECKING:
    from apps.assignments.models import Assignment
    from apps.organization.models import OrgUnit
    from apps.personnel.models import Person


class AssignmentService:
    """
    Бізнес-логіка роботи з призначеннями військовослужбовців.
    """

    @staticmethod
    def get_current(person: Person) -> Assignment | None:
        """
        Повертає поточне активне призначення військовослужбовця.
        """
        return AssignmentSelector.current(person)

    @classmethod
    def get_current_or_raise(cls, person: Person) -> Assignment:
        """
        Повертає поточне активне призначення або генерує помилку.
        """
        assignment = cls.get_current(person)

        if assignment is None:
            raise ValidationError(
                "У військовослужбовця відсутнє активне призначення."
            )

        return assignment

    @classmethod
    def get_current_unit(cls, person: Person) -> OrgUnit:
        """
        Повертає поточний структурний підрозділ військовослужбовця.
        """
        return cls.get_current_or_raise(person).staff_position.org_unit

    @staticmethod
    def get_active_personnel(org_unit: OrgUnit):
        """
        Повертає активні призначення підрозділу.
        """
        return AssignmentSelector.active_by_unit(org_unit)

    @staticmethod
    def get_active_personnel_count(org_unit: OrgUnit) -> int:
        """
        Повертає кількість військовослужбовців
        з активними призначеннями.
        """
        return AssignmentSelector.active_count_by_unit(org_unit)
