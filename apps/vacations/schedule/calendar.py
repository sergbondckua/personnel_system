from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, frozen=True)
class CalendarDay:
    """
    Один день календаря.
    """

    date: date
    day: int
    weekday: int
    weekday_short: str
    is_today: bool
    is_weekend: bool


class CalendarService:
    """
    Побудова календаря для графіків.
    """

    @staticmethod
    def month(year: int, month: int) -> list[CalendarDay]:
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
