from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MonthNavigation:
    """
    Дані для навігації між місяцями.
    """

    previous_year: int
    previous_month: int

    current_year: int
    current_month: int

    next_year: int
    next_month: int


class NavigationService:
    """
    Навігація між місяцями.
    """

    @staticmethod
    def build(year: int, month: int) -> MonthNavigation:
        if month == 1:
            previous_year = year - 1
            previous_month = 12
        else:
            previous_year = year
            previous_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1

        return MonthNavigation(
            previous_year=previous_year,
            previous_month=previous_month,
            current_year=year,
            current_month=month,
            next_year=next_year,
            next_month=next_month,
        )
