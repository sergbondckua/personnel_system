from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.vacations.enums import VacationStatus


class VacationService:
    """
    Бізнес-логіка роботи з відпустками.
    """

    @classmethod
    def validate(cls, vacation) -> None:
        """
        Виконує всі перевірки відпустки.
        """
        cls.validate_dates(vacation)
        cls.validate_days(vacation)
        cls.validate_overlap(vacation)

    @staticmethod
    def validate_dates(vacation) -> None:
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
    def validate_days(vacation) -> None:
        """
        Перевіряє кількість діб та річний ліміт виду відпустки.
        """
        if vacation.days <= 0:
            raise ValidationError(
                {"days": ("Кількість діб повинна бути більшою за нуль.")}
            )

        vacation_type = vacation.vacation_type

        if vacation_type.annual_limit is None:
            return

        used_days = (
            vacation.__class__.objects.filter(
                person=vacation.person,
                vacation_type=vacation_type,
                status__in=[
                    VacationStatus.APPROVED,
                    VacationStatus.ACTIVE,
                    VacationStatus.COMPLETED,
                ],
                date_from__year=vacation.date_from.year,
            )
            .exclude(pk=vacation.pk)
            .values_list("days", flat=True)
        )

        if sum(used_days) + vacation.days > vacation_type.annual_limit:
            raise ValidationError(
                {
                    "days": (
                        f"Перевищено річний ліміт "
                        f"({vacation_type.annual_limit} діб)."
                    )
                }
            )

    @staticmethod
    def validate_overlap(vacation) -> None:
        """
        Перевіряє відсутність перетину з іншими відпустками.
        """
        overlap = (
            vacation.__class__.objects.filter(
                person=vacation.person,
            )
            .exclude(pk=vacation.pk)
            .exclude(status=VacationStatus.CANCELED)
            .filter(
                Q(date_from__lte=vacation.date_to),
                Q(date_to__gte=vacation.date_from),
            )
        )

        if overlap.exists():
            raise ValidationError(
                {
                    "date_from": (
                        "У військовослужбовця вже існує відпустка "
                        "на цей період."
                    )
                }
            )
