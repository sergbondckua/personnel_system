from __future__ import annotations

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


@dataclass(slots=True, frozen=True)
class CalendarMonth:
    """
    Один місяць календаря.
    """

    number: int
    name: str
    days: list[CalendarDay]


@dataclass(slots=True, frozen=True)
class CalendarYear:
    """
    Календар року.
    """

    year: int
    months: list[CalendarMonth]

    @property
    def total_days(self) -> int:
        """
        Загальна кількість днів року.
        """

        return sum(len(month.days) for month in self.months)
