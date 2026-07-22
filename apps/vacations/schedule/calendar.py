from __future__ import annotations

import calendar
from datetime import date
from apps.common.localization.months import get_month
from apps.vacations.schedule.calendar_models import (
    CalendarDay,
    CalendarMonth,
    CalendarYear,
)


class CalendarService:
    """
    Побудова календаря для графіків.
    """

    @staticmethod
    def build_month(year: int, month: int) -> list[CalendarDay]:
        """
        Повертає всі дні місяця.
        """

        today = date.today()

        _, days = calendar.monthrange(year, month)

        result: list[CalendarDay] = []
        WEEKDAYS = (
            "Пн",
            "Вт",
            "Ср",
            "Чт",
            "Пт",
            "Сб",
            "Нд",
        )

        for day in range(1, days + 1):
            current = date(year, month, day)

            result.append(
                CalendarDay(
                    date=current,
                    day=day,
                    weekday=current.weekday(),
                    weekday_short=WEEKDAYS[current.weekday()],
                    is_today=current == today,
                    is_weekend=current.weekday() >= 5,
                )
            )

        return result

    @staticmethod
    def build_year(
        year: int,
    ) -> CalendarYear:
        """
        Побудова календаря року.
        """

        months: list[CalendarMonth] = []

        for month in range(1, 13):
            months.append(
                CalendarMonth(
                    number=month,
                    name=get_month(month).nominative,
                    days=CalendarService.build_month(
                        year,
                        month,
                    ),
                )
            )

        return CalendarYear(
            year=year,
            months=months,
        )
