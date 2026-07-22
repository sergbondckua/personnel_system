from datetime import date, timedelta

from apps.organization.tree_node import OrgTreeNode
from apps.vacations.selectors import VacationSelector


class VacationScheduleBuilder:
    """
    Заповнює дерево організації інформацією про відпустки.
    """

    @classmethod
    def fill(
        cls,
        tree: list[OrgTreeNode],
        date_from: date,
        date_to: date,
    ) -> None:
        vacations = VacationSelector.for_period(
            date_from,
            date_to,
        )

        people = {}

        cls._collect_people(tree, people)

        for vacation in vacations:
            person = people.get(vacation.person_id)

            if person is None:
                continue

            current = max(
                vacation.date_from,
                date_from,
            )

            last = min(
                vacation.date_to,
                date_to,
            )

            while current <= last:
                person.schedule[current] = vacation
                current += timedelta(days=1)

    @classmethod
    def _collect_people(
        cls,
        nodes: list[OrgTreeNode],
        people: dict,
    ) -> None:
        """
        Збирає всіх військовослужбовців дерева.
        """

        for node in nodes:
            for person in node.people:
                people[person.assignment.person_id] = person

            cls._collect_people(
                node.children,
                people,
            )
