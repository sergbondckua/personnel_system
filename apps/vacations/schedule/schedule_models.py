from __future__ import annotations

from dataclasses import dataclass

from .calendar_models import CalendarYear


@dataclass(slots=True, frozen=True)
class ScheduleCell:
    """
    Одна клітинка графіка.
    """

    active: bool


@dataclass(slots=True)
class SchedulePerson:
    """
    Один військовослужбовець.
    """

    assignment: object

    cells: list[ScheduleCell]


@dataclass(slots=True)
class ScheduleUnit:
    """
    Один підрозділ.
    """

    unit: object

    people: list[SchedulePerson]

    children: list["ScheduleUnit"]


@dataclass(slots=True)
class VacationSchedule:
    """
    Повний графік відпусток.
    """

    calendar: CalendarYear

    units: list[ScheduleUnit]
