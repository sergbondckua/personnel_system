from __future__ import annotations


from apps.vacations.schedule.calendar import CalendarService
from apps.vacations.schedule.schedule_models import (
    ScheduleCell,
    SchedulePerson,
    ScheduleUnit,
    VacationSchedule,
)
from apps.organization.tree import OrganizationTreeService


class VacationScheduleBuilder:
    """
    Побудова графіка відпусток.
    """

    @staticmethod
    def build(year: int) -> VacationSchedule:

        calendar = CalendarService.build_year(year)

        tree = OrganizationTreeService.build()

        units = [
            VacationScheduleBuilder._build_unit(
                unit,
                calendar,
            )
            for unit in tree
        ]

        return VacationSchedule(
            calendar=calendar,
            units=units,
        )

    @staticmethod
    def _build_unit(
        node,
        calendar,
    ) -> ScheduleUnit:

        people = [
            VacationScheduleBuilder._build_person(
                person,
                calendar,
            )
            for person in node.people
        ]

        children = [
            VacationScheduleBuilder._build_unit(
                child,
                calendar,
            )
            for child in node.children
        ]

        return ScheduleUnit(
            unit=node.unit,
            people=people,
            children=children,
        )

    @staticmethod
    def _build_person(
        person,
        calendar,
    ) -> SchedulePerson:

        cells: list[ScheduleCell] = []

        for month in calendar.months:
            for day in month.days:
                cells.append(
                    ScheduleCell(
                        active=day.date in person.schedule,
                    )
                )

        return SchedulePerson(
            assignment=person.assignment,
            cells=cells,
        )
