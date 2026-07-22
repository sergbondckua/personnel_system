from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.db.models import QuerySet

from apps.vacations.enums import VacationStatus

if TYPE_CHECKING:
    from apps.organization.models import OrgUnit
    from apps.personnel.models import Person
    from apps.references.models import VacationType
    from apps.vacations.models import Vacation

Vacation = apps.get_model("vacations", "Vacation")


class VacationSelector:
    """
    ORM-запити для роботи з відпустками.

    Selector не містить бізнес-логіки та використовується
    виключно для отримання даних із бази.
    """

    @staticmethod
    def for_person(person: Person) -> QuerySet[Any]:
        """
        Повертає всі відпустки військовослужбовця.
        """
        return Vacation.objects.filter(person=person)

    @staticmethod
    def overlapping(vacation: Vacation) -> QuerySet[Any]:
        """
        Повертає відпустки, що перетинаються з указаною.
        """
        return (
            Vacation.objects.filter(
                person=vacation.person,
            )
            .exclude(pk=vacation.pk)
            .exclude(status=VacationStatus.CANCELED)
            .filter(
                date_from__lte=vacation.date_to,
                date_to__gte=vacation.date_from,
            )
        )

    @staticmethod
    def used_days(
        person: Person,
        vacation_type: VacationType,
        year: int,
        exclude_pk: int | None = None,
    ) -> QuerySet[Any]:
        """
        Повертає відпустки, які враховуються
        при розрахунку річного ліміту.
        """
        queryset = Vacation.objects.filter(
            person=person,
            vacation_type=vacation_type,
            status__in=(
                VacationStatus.APPROVED,
                VacationStatus.ACTIVE,
                VacationStatus.COMPLETED,
            ),
            date_from__year=year,
        )

        if exclude_pk is not None:
            queryset = queryset.exclude(pk=exclude_pk)

        return queryset

    @staticmethod
    def active_in_unit(
        org_unit: OrgUnit,
        date_from: date,
        date_to: date,
        exclude_pk: int | None = None,
    ) -> QuerySet[Any]:
        """
        Повертає всі відпустки військовослужбовців
        підрозділу, які перетинаються з указаним періодом.
        """
        queryset = (
            Vacation.objects.filter(
                person__assignments__is_active=True,
                person__assignments__staff_position__org_unit=org_unit,
            )
            .exclude(
                status=VacationStatus.CANCELED,
            )
            .filter(
                date_from__lte=date_to,
                date_to__gte=date_from,
            )
        )

        if exclude_pk is not None:
            queryset = queryset.exclude(pk=exclude_pk)

        return queryset.distinct()

    @staticmethod
    def for_period(date_from: date, date_to: date):
        """
        Повертає всі відпустки, що перетинаються із заданим періодом.
        """

        return Vacation.objects.select_related(
            "person",
            "vacation_type",
        ).filter(
            date_from__lte=date_to,
            date_to__gte=date_from,
        )
