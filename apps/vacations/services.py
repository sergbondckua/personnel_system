from __future__ import annotations

import math
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.assignments.services import AssignmentService
from apps.vacations.selectors import VacationSelector

if TYPE_CHECKING:
    from apps.vacations.models import Vacation


class VacationService:
    """
    Бізнес-логіка роботи з відпустками.
    """

    @classmethod
    def validate(cls, vacation: Vacation) -> None:
        """
        Виконує всі бізнес-перевірки відпустки.

        Args:
            vacation: Об'єкт відпустки.
        """
        cls.validate_dates(vacation)
        cls.validate_days(vacation)
        cls.validate_overlap(vacation)
        cls.validate_unit_limit(vacation)

    @staticmethod
    def validate_dates(vacation: Vacation) -> None:
        """
        Перевіряє коректність дат.
        """
        if vacation.date_from > vacation.date_to:
            raise ValidationError(
                {
                    "date_to": (
                        "Дата закінчення не може бути раніше дати початку."
                    )
                }
            )

    @staticmethod
    def validate_days(vacation: Vacation) -> None:
        """
        Перевіряє кількість діб та річний ліміт.
        """

        vacation_type = vacation.vacation_type

        if vacation_type.annual_limit is None:
            return

        vacations = VacationSelector.used_days(
            person=vacation.person,
            vacation_type=vacation_type,
            year=vacation.date_from.year,
            exclude_pk=vacation.pk,
        )

        used_days = sum(item.days for item in vacations)

        if used_days + vacation.days > vacation_type.annual_limit:
            raise ValidationError(
                {
                    "days": (
                        f"Перевищено річний ліміт "
                        f"({vacation_type.annual_limit} діб)."
                    )
                }
            )

    @staticmethod
    def validate_overlap(vacation: Vacation) -> None:
        """
        Перевіряє перетин відпусток.
        """
        if VacationSelector.overlapping(vacation).exists():
            raise ValidationError(
                "У військовослужбовця вже існує відпустка на цей період."
            )

    @staticmethod
    def validate_unit_limit(vacation: Vacation) -> None:
        """
        Перевіряє, що кількість військовослужбовців
        у відпустці не перевищує допустимий відсоток
        у структурному підрозділі.
        """
        unit = AssignmentService.get_current_unit(vacation.person)

        personnel_count = AssignmentService.get_active_personnel_count(unit)

        if personnel_count == 0:
            return

        vacations_count = VacationSelector.active_in_unit(
            org_unit=unit,
            date_from=vacation.date_from,
            date_to=vacation.date_to,
            exclude_pk=vacation.pk,
        ).count()

        limit = max(
            1,
            math.ceil(
                personnel_count * settings.VACATION_MAX_UNIT_PERCENT / 100
            ),
        )

        if vacations_count + 1 > limit:
            raise ValidationError(
                (
                    "Перевищено допустиму кількість "
                    "військовослужбовців, які можуть "
                    "одночасно перебувати у відпустці "
                    "в цьому підрозділі."
                )
            )
