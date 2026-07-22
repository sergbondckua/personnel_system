from __future__ import annotations

from collections import defaultdict

from apps.assignments.selectors import AssignmentSelector
from apps.organization.models import OrgUnit
from apps.organization.tree_node import OrgTreeNode
from apps.organization.tree_person import OrgTreePerson


class OrganizationTreeService:
    """
    Побудова дерева організаційної структури.
    """

    @classmethod
    def build(cls, schedule: dict | None = None) -> list[OrgTreeNode]:
        """
        Повертає дерево підрозділів
        разом із військовослужбовцями.
        """

        units = list(
            OrgUnit.objects.select_related(
                "organization",
                "type",
                "parent",
            ).order_by(
                "organization",
                "sort_order",
                "name",
            )
        )

        assignments = list(AssignmentSelector.all_active())

        people_by_unit = defaultdict(list)

        schedule = schedule or {}

        for assignment in assignments:
            people_by_unit[assignment.staff_position.org_unit_id].append(
                OrgTreePerson(
                    assignment=assignment,
                    schedule=schedule.get(
                        assignment.person_id,
                        {},
                    ),
                )
            )

        nodes: dict[int, OrgTreeNode] = {}

        roots: list[OrgTreeNode] = []

        for unit in units:
            nodes[unit.id] = OrgTreeNode(
                unit=unit,
                people=people_by_unit.get(unit.id, []),
            )

        for unit in units:
            node = nodes[unit.id]

            if unit.parent_id is None:
                roots.append(node)

            else:
                parent = nodes[unit.parent_id]
                node.level = parent.level + 1
                parent.children.append(node)

        return roots
