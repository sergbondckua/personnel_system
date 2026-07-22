from dataclasses import dataclass, field
from datetime import date

from apps.assignments.models import Assignment
from apps.vacations.models import Vacation


@dataclass(slots=True)
class OrgTreePerson:
    """
    Військовослужбовець у дереві структури.
    """

    assignment: Assignment

    schedule: dict[date, Vacation] = field(default_factory=dict)