from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Month:
    """
    Назва місяця.
    """

    nominative: str
    genitive: str


MONTHS: dict[int, Month] = {
    1: Month("Січень", "січня"),
    2: Month("Лютий", "лютого"),
    3: Month("Березень", "березня"),
    4: Month("Квітень", "квітня"),
    5: Month("Травень", "травня"),
    6: Month("Червень", "червня"),
    7: Month("Липень", "липня"),
    8: Month("Серпень", "серпня"),
    9: Month("Вересень", "вересня"),
    10: Month("Жовтень", "жовтня"),
    11: Month("Листопад", "листопада"),
    12: Month("Грудень", "грудня"),
}


def get_month(month: int) -> Month:
    """
    Повертає інформацію про місяць.
    """

    return MONTHS[month]
