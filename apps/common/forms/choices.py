from __future__ import annotations

from datetime import date

from apps.common.localization.months import MONTHS


def year_choices(
    years_back: int = 2,
    years_forward: int = 5,
) -> list[tuple[int, str]]:
    """
    Список років.
    """

    current = date.today().year

    return [
        (
            year,
            str(year),
        )
        for year in range(
            current - years_back,
            current + years_forward + 1,
        )
    ]


def month_choices() -> list[tuple[int, str]]:
    """
    Список місяців.
    """

    return [
        (
            number,
            month.nominative,
        )
        for number, month in MONTHS.items()
    ]
