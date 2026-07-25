from dataclasses import dataclass, field
from datetime import date

from apps.assignments.models import Assignment
from apps.vacations.models import Vacation


@dataclass(slots=True)
class ScheduleCell:
    date: date
    vacation: Vacation | None = None


@dataclass(slots=True)
class OrgTreePerson:
    assignment: Assignment

    schedule: dict[date, Vacation] = field(default_factory=dict)

    cells: list[ScheduleCell] = field(default_factory=list)